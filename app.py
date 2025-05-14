from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# -------- BANCO DE DADOS --------
def conectar():
    conn = sqlite3.connect("database.db")
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
    conn.commit()
    conn.close()


# Cria as tabelas se não existirem
criar_tabelas()


# -------- ROTA INICIAL --------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -------- CADASTRO DE RESÍDUO --------
@app.route("/cadastro-residuo", methods=["GET", "POST"])
def cadastro_residuo():
    if request.method == "POST":
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        risco = request.form["risco"]
        instrucoes = request.form["instrucoes"]
        conn = conectar()
        conn.execute(
            "INSERT INTO residuos (nome, tipo, risco, instrucoes) VALUES (?, ?, ?, ?)",
            (nome, tipo, risco, instrucoes),
        )
        conn.commit()
        conn.close()
        return redirect("/dashboard")
    return render_template("cadastro-residuo.html")


# -------- CADASTRO DE EMPRESAS --------
@app.route("/empresas", methods=["GET", "POST"])
def empresas():
    if request.method == "POST":
        nome = request.form["nome"]
        cnpj = request.form["cnpj"]
        licenca = request.form["licenca"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        conn = conectar()
        conn.execute(
            "INSERT INTO empresas (nome, cnpj, licenca, telefone, email) VALUES (?, ?, ?, ?, ?)",
            (nome, cnpj, licenca, telefone, email),
        )
        conn.commit()
        conn.close()
        return redirect("/dashboard")
    return render_template("empresas.html")


# -------- REGISTRAR DESCARTE --------
@app.route("/registro-descarte", methods=["GET", "POST"])
def registro_descarte():
    conn, cursor = conectar()  # Obtenha a conexão e o cursor

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
        return redirect("/dashboard")

    conn.close()
    return render_template(
        "registro-descarte.html", residuos=residuos, empresas=empresas
    )


# -------- RELATÓRIOS --------
@app.route("/relatorios")
def relatorios():
    conn, cursor = conectar()  # Obtenha a conexão e o cursor

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


# -------- ROTA DE LOGIN --------
@app.route("/login", methods=["POST"])
def login():
    return redirect("/dashboard")


# -------- INICIAR SERVIDOR --------
if __name__ == "__main__":
    app.run(debug=True)
