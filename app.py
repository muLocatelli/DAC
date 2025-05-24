from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib  # Para hash de senhas

app = Flask(__name__)

# -------- BANCO DE DADOS --------
def conectar():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    conn, cursor = conectar()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS residuos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            risco TEXT,
            instrucoes TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cnpj TEXT,
            licenca TEXT,
            telefone TEXT,
            email TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS descartes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            peso REAL,
            id_residuo INTEGER,
            id_empresa INTEGER,
            FOREIGN KEY (id_residuo) REFERENCES residuos(id),
            FOREIGN KEY (id_empresa) REFERENCES empresas(id)
        )
    """)
    # Nova tabela para usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            cep TEXT,
            senha_hash TEXT NOT NULL
        )
    """)
    # Inserir o usuário "medcycle" com senha "12345" se não existir
    senha_padrao_hash = hashlib.sha256("12345".encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE email = 'medcycle'")
    usuario_padrao = cursor.fetchone()
    if not usuario_padrao:
        cursor.execute(
            "INSERT INTO users (nome, sobrenome, email, cpf, telefone, cep, senha_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("Med", "Cycle", "medcycle", "00000000000", None, None, senha_padrao_hash),
        )
        conn.commit()

    conn.commit()
    conn.close()

# Cria as tabelas se não existirem
criar_tabelas()

# Função auxiliar para hash de senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# -------- ROTAS --------
@app.route("/")
def index():
    # Esta é a sua página de login
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        email = request.form["email"]
        cpf = request.form["cpf"]
        telefone = request.form.get("telefone") # Use .get para campos opcionais
        cep = request.form.get("cep")         # Use .get para campos opcionais
        senha = request.form["senha"]
        confirma_senha = request.form["confirma_senha"]

        if senha != confirma_senha:
            # Em um app real, você mostraria uma mensagem de erro na tela
            print("Erro: As senhas não coincidem!")
            return render_template("cadastro.html", erro="As senhas não coincidem!")

        senha_hashed = hash_senha(senha)

        conn, cursor = conectar()
        try:
            cursor.execute(
                "INSERT INTO users (nome, sobrenome, email, cpf, telefone, cep, senha_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nome, sobrenome, email, cpf, telefone, cep, senha_hashed),
            )
            conn.commit()
            # Redireciona para a página de login após o cadastro bem-sucedido
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            # Isso acontece se o email ou CPF já existirem (UNIQUE constraint)
            print("Erro: Email ou CPF já cadastrados.")
            return render_template("cadastro.html", erro="Email ou CPF já cadastrados.")
        finally:
            conn.close()

    # Se for um GET request, apenas renderiza o formulário de cadastro
    return render_template("cadastro.html")

@app.route("/login", methods=["POST"])
def login_post():
    usuario = request.form["usuario"]
    senha = request.form["senha"]
    senha_hashed = hash_senha(senha)

    conn, cursor = conectar()
    cursor.execute("SELECT * FROM users WHERE email = ?", (usuario,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute("SELECT * FROM users WHERE email = ? AND senha_hash = ?", (usuario, senha_hashed))
        user = cursor.fetchone()
        conn.close()
        if user:
            print(f"Login bem-sucedido para: {user['email']}")
            return redirect(url_for("dashboard"))
        else:
            print("Login falhou: Senha incorreta.")
            return render_template("index.html", erro_login="Senha incorreta")
    else:
        conn.close()
        print("Login falhou: Usuário inexistente.")
        return render_template("index.html", erro_login="Usuário incorreto")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/cadastro-residuo", methods=["GET", "POST"])
def cadastro_residuo():
    if request.method == "POST":
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        risco = request.form["risco"]
        instrucoes = request.form["instrucoes"]
        conn, cursor = conectar()
        cursor.execute(
            "INSERT INTO residuos (nome, tipo, risco, instrucoes) VALUES (?, ?, ?, ?)",
            (nome, tipo, risco, instrucoes),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    return render_template("cadastro-residuo.html")

@app.route("/empresas", methods=["GET", "POST"])
def empresas():
    if request.method == "POST":
        nome = request.form["nome"]
        cnpj = request.form["cnpj"]
        licenca = request.form["licenca"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        conn, cursor = conectar()
        cursor.execute(
            "INSERT INTO empresas (nome, cnpj, licenca, telefone, email) VALUES (?, ?, ?, ?, ?)",
            (nome, cnpj, licenca, telefone, email),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    return render_template("empresas.html")

@app.route("/registro-descarte", methods=["GET", "POST"])
def registro_descarte():
    conn, cursor = conectar()
    cursor.execute("SELECT id, nome FROM residuos")
    residuos = cursor.fetchall()
    cursor.execute("SELECT id, nome FROM empresas")
    empresas = cursor.fetchall()

    if request.method == "POST":
        data = request.form["data"]
        peso = request.form["peso"]
        id_residuo = request.form["residuo"]
        id_empresa = request.form["empresa"]
        cursor.execute(
            "INSERT INTO descartes (data, peso, id_residuo, id_empresa) VALUES (?, ?, ?, ?)",
            (data, peso, id_residuo, id_empresa),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    conn.close()
    return render_template(
        "registro-descarte.html", residuos=residuos, empresas=empresas
    )

@app.route("/relatorios")
def relatorios():
    conn, cursor = conectar()
    cursor.execute("SELECT COUNT(*) FROM residuos")
    total_residuos = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(peso) FROM descartes")
    resultado_peso = cursor.fetchone()
    total_kg = (
        resultado_peso[0] if resultado_peso and resultado_peso[0] is not None else 0
    )

    cursor.execute("""
        SELECT empresas.nome, COUNT(*) as freq FROM descartes
        JOIN empresas ON empresas.id = descartes.id_empresa
        GROUP BY empresas.nome ORDER BY freq DESC LIMIT 1
    """)
    empresa_frequente = cursor.fetchone()

    conn.close()
    return render_template(
        "relatorios.html",
        total_residuos=total_residuos,
        total_kg=total_kg,
        empresa=empresa_frequente,
    )

# -------- ROTAS PARA RELATÓRIOS INDIVIDUALIZADOS --------
@app.route("/reciclaveis.html")
def relatorio_reciclaveis():
    return render_template("reciclaveis.html")

@app.route("/perfurante.html")
def relatorio_perfurante():
    return render_template("perfurante.html")

@app.route("/quimico.html")
def relatorio_quimico():
    return render_template("quimico.html")

@app.route("/infectante.html")
def relatorio_infectante():
    return render_template("infectante.html")

# -------- NOVA ROTA PARA O PERFIL --------
@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

# -------- NOVA ROTA PARA FALE CONOSCO --------
@app.route("/fale_conosco")
def fale_conosco():
    conn, cursor = conectar()
    cursor.execute("SELECT id, nome FROM residuos")
    residuos = cursor.fetchall()
    cursor.execute("SELECT id, nome FROM empresas")
    empresas = cursor.fetchall()
    conn.close()
    return render_template("fale_conosco.html", residuos=residuos, empresas=empresas)

# -------- NOVA ROTA PARA CADASTRO DE EMPRESA --------
@app.route("/cadastro_empresa", methods=["GET"])
def cadastro_empresa():
    return render_template("cadastro_empresa.html")

# -------- INICIAR SERVIDOR --------
if __name__ == "__main__":
    app.run(debug=True)