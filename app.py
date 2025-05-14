from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -------- BANCO DE DADOS --------
def conectar():
    return sqlite3.connect("database.db")

# -------- ROTA INICIAL --------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# -------- CADASTRO DE RESÍDUO --------
@app.route('/cadastro-residuo', methods=['GET', 'POST'])
def cadastro_residuo():
    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        risco = request.form['risco']
        instrucoes = request.form['instrucoes']
        conn = conectar()
        conn.execute("INSERT INTO residuos (nome, tipo, risco, instrucoes) VALUES (?, ?, ?, ?)",
                     (nome, tipo, risco, instrucoes))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template('cadastro-residuo.html')

# -------- CADASTRO DE EMPRESAS --------
@app.route('/empresas', methods=['GET', 'POST'])
def empresas():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        licenca = request.form['licenca']
        telefone = request.form['telefone']
        email = request.form['email']
        conn = conectar()
        conn.execute("INSERT INTO empresas (nome, cnpj, licenca, telefone, email) VALUES (?, ?, ?, ?, ?)",
                     (nome, cnpj, licenca, telefone, email))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template('empresas.html')

# -------- REGISTRAR DESCARTE --------
@app.route('/registro-descarte', methods=['GET', 'POST'])
def registro_descarte():
    conn = conectar()
    residuos = conn.execute("SELECT id, nome FROM residuos").fetchall()
    empresas = conn.execute("SELECT id, nome FROM empresas").fetchall()

    if request.method == 'POST':
        data = request.form['data']
        peso = request.form['peso']
        id_residuo = request.form['residuo']
        id_empresa = request.form['empresa']
        conn.execute("INSERT INTO descartes (data, peso, id_residuo, id_empresa) VALUES (?, ?, ?, ?)",
                     (data, peso, id_residuo, id_empresa))
        conn.commit()
        conn.close()
        return redirect('/dashboard')

    conn.close()
    return render_template('registro-descarte.html', residuos=residuos, empresas=empresas)

# -------- RELATÓRIOS --------
@app.route('/relatorios')
def relatorios():
    conn = conectar()
    total_residuos = conn.execute("SELECT COUNT(*) FROM residuos").fetchone()[0]
    total_kg = conn.execute("SELECT SUM(peso) FROM descartes").fetchone()[0] or 0
    empresa_frequente = conn.execute("""
        SELECT empresas.nome, COUNT(*) as freq FROM descartes
        JOIN empresas ON empresas.id = descartes.id_empresa
        GROUP BY empresas.nome ORDER BY freq DESC LIMIT 1
    """).fetchone()
    conn.close()
    return render_template('relatorios.html', total_residuos=total_residuos, total_kg=total_kg, empresa=empresa_frequente)

# -------- INICIAR SERVIDOR --------
if __name__ == '__main__':
    app.run(debug=True)
