
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from database import criar_tabelas, conectar_banco


# ==========================================
# ALGORITMO DE BUSCA LINEAR
# ==========================================

def buscar_pacientes(pacientes, nome_procurado):
    resultados = []

    indice = 0

    while indice < len(pacientes):
        paciente = pacientes[indice]
        nome = paciente["nome"].lower()

        if nome_procurado.lower() in nome:
            resultados.append(paciente)

        indice += 1

    return resultados

# ==========================================
# CONFIGURAÇÃO DO SISTEMA
# ==========================================

app = Flask(__name__)
app.secret_key = "sorriso-facil-chave-local"

criar_tabelas()


# ==========================================
# PÁGINA INICIAL
# ==========================================

@app.route("/")
def inicio():
    conexao = conectar_banco()

    total_pacientes = conexao.execute(
        "SELECT COUNT(*) FROM pacientes"
    ).fetchone()[0]

    total_consultas = conexao.execute(
        "SELECT COUNT(*) FROM consultas"
    ).fetchone()[0]

    conexao.close()

    return render_template(
        "index.html",
        total_pacientes=total_pacientes,
        total_consultas=total_consultas
    )


# ==========================================
# PACIENTES - LISTAR E PESQUISAR
# ==========================================

@app.route("/pacientes")
def listar_pacientes():
    busca = request.args.get("busca", "").strip()

    conexao = conectar_banco()

    pacientes = conexao.execute(
        """
        SELECT *
        FROM pacientes
        ORDER BY nome ASC
        """
    ).fetchall()

    conexao.close()

    if busca:
        pacientes = buscar_pacientes(pacientes, busca)

    return render_template(
        "pacientes.html",
        pacientes=pacientes,
        busca=busca
    )


# ==========================================
# PACIENTES - CADASTRAR
# ==========================================

@app.route("/pacientes/novo", methods=["GET", "POST"])
def novo_paciente():

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not telefone:
            flash("Preencha o nome e o telefone.")
            return redirect(url_for("novo_paciente"))

        conexao = conectar_banco()

        conexao.execute(
            """
            INSERT INTO pacientes (nome, telefone, email)
            VALUES (?, ?, ?)
            """,
            (nome, telefone, email)
        )

        conexao.commit()
        conexao.close()

        flash("Paciente cadastrado com sucesso!")

        return redirect(url_for("listar_pacientes"))

    return render_template(
        "paciente_form.html",
        titulo="Cadastrar paciente",
        paciente=None
    )


# ==========================================
# PACIENTES - EDITAR
# ==========================================

@app.route("/pacientes/editar/<int:id>", methods=["GET", "POST"])
def editar_paciente(id):

    conexao = conectar_banco()

    paciente = conexao.execute(
        "SELECT * FROM pacientes WHERE id = ?",
        (id,)
    ).fetchone()

    if paciente is None:
        conexao.close()
        flash("Paciente não encontrado.")
        return redirect(url_for("listar_pacientes"))

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not telefone:
            conexao.close()
            flash("Preencha o nome e o telefone.")
            return redirect(url_for("editar_paciente", id=id))

        conexao.execute(
            """
            UPDATE pacientes
            SET nome = ?, telefone = ?, email = ?
            WHERE id = ?
            """,
            (nome, telefone, email, id)
        )

        conexao.commit()
        conexao.close()

        flash("Paciente atualizado com sucesso!")

        return redirect(url_for("listar_pacientes"))

    conexao.close()

    return render_template(
        "paciente_form.html",
        titulo="Editar paciente",
        paciente=paciente
    )


# ==========================================
# PACIENTES - EXCLUIR
# ==========================================

@app.route("/pacientes/excluir/<int:id>", methods=["POST"])
def excluir_paciente(id):

    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM pacientes WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    flash("Paciente excluído.")

    return redirect(url_for("listar_pacientes"))


# ==========================================
# CONSULTAS - LISTAR
# ==========================================

@app.route("/consultas")
def listar_consultas():

    busca = request.args.get("busca", "").strip()

    conexao = conectar_banco()

    consultas = conexao.execute(
        """
        SELECT
            consultas.id,
            consultas.paciente_id,
            consultas.data,
            consultas.horario,
            consultas.procedimento,
            consultas.status,
            pacientes.nome AS nome_paciente

        FROM consultas

        INNER JOIN pacientes
        ON consultas.paciente_id = pacientes.id

        WHERE pacientes.nome LIKE ?
        OR consultas.procedimento LIKE ?

        ORDER BY consultas.data ASC, consultas.horario ASC
        """,
        (f"%{busca}%", f"%{busca}%")
    ).fetchall()

    conexao.close()

    return render_template(
        "consultas.html",
        consultas=consultas,
        busca=busca
    )


# ==========================================
# CONSULTAS - CADASTRAR
# ==========================================

@app.route("/consultas/nova", methods=["GET", "POST"])
def nova_consulta():

    conexao = conectar_banco()

    pacientes = conexao.execute(
        "SELECT * FROM pacientes ORDER BY nome ASC"
    ).fetchall()

    if not pacientes:
        conexao.close()
        flash("Cadastre um paciente antes de agendar uma consulta.")
        return redirect(url_for("listar_pacientes"))

    if request.method == "POST":

        paciente_id = request.form.get("paciente_id", "").strip()
        data = request.form.get("data", "").strip()
        horario = request.form.get("horario", "").strip()
        procedimento = request.form.get("procedimento", "").strip()
        status = request.form.get("status", "Agendada").strip()

        paciente_existe = conexao.execute(
            "SELECT id FROM pacientes WHERE id = ?",
            (paciente_id,)
        ).fetchone()

        if not paciente_existe or not data or not horario or not procedimento:
            conexao.close()
            flash("Preencha todos os campos corretamente.")
            return redirect(url_for("nova_consulta"))

        if status not in ["Agendada", "Realizada", "Cancelada"]:
            status = "Agendada"

        conexao.execute(
            """
            INSERT INTO consultas
            (paciente_id, data, horario, procedimento, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (paciente_id, data, horario, procedimento, status)
        )

        conexao.commit()
        conexao.close()

        flash("Consulta cadastrada com sucesso!")

        return redirect(url_for("listar_consultas"))

    conexao.close()

    return render_template(
        "consulta_form.html",
        titulo="Cadastrar consulta",
        pacientes=pacientes,
        consulta=None
    )


# ==========================================
# CONSULTAS - EDITAR
# ==========================================

@app.route("/consultas/editar/<int:id>", methods=["GET", "POST"])
def editar_consulta(id):

    conexao = conectar_banco()

    consulta = conexao.execute(
        "SELECT * FROM consultas WHERE id = ?",
        (id,)
    ).fetchone()

    pacientes = conexao.execute(
        "SELECT * FROM pacientes ORDER BY nome ASC"
    ).fetchall()

    if consulta is None:
        conexao.close()
        flash("Consulta não encontrada.")
        return redirect(url_for("listar_consultas"))

    if request.method == "POST":

        paciente_id = request.form.get("paciente_id", "").strip()
        data = request.form.get("data", "").strip()
        horario = request.form.get("horario", "").strip()
        procedimento = request.form.get("procedimento", "").strip()
        status = request.form.get("status", "Agendada").strip()

        paciente_existe = conexao.execute(
            "SELECT id FROM pacientes WHERE id = ?",
            (paciente_id,)
        ).fetchone()

        if not paciente_existe or not data or not horario or not procedimento:
            conexao.close()
            flash("Preencha todos os campos corretamente.")
            return redirect(url_for("editar_consulta", id=id))

        if status not in ["Agendada", "Realizada", "Cancelada"]:
            status = "Agendada"

        conexao.execute(
            """
            UPDATE consultas
            SET paciente_id = ?,
                data = ?,
                horario = ?,
                procedimento = ?,
                status = ?
            WHERE id = ?
            """,
            (paciente_id, data, horario, procedimento, status, id)
        )

        conexao.commit()
        conexao.close()

        flash("Consulta atualizada com sucesso!")

        return redirect(url_for("listar_consultas"))

    conexao.close()

    return render_template(
        "consulta_form.html",
        titulo="Editar consulta",
        pacientes=pacientes,
        consulta=consulta
    )


# ==========================================
# CONSULTAS - EXCLUIR
# ==========================================

@app.route("/consultas/excluir/<int:id>", methods=["POST"])
def excluir_consulta(id):

    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM consultas WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    flash("Consulta excluída.")

    return redirect(url_for("listar_consultas"))


# ==========================================
# API - PACIENTES EM JSON
# ==========================================

@app.route("/api/pacientes")
def api_pacientes():

    conexao = conectar_banco()

    pacientes = conexao.execute(
        "SELECT * FROM pacientes ORDER BY nome ASC"
    ).fetchall()

    conexao.close()

    resultado = []

    for paciente in pacientes:
        resultado.append({
            "id": paciente["id"],
            "nome": paciente["nome"],
            "telefone": paciente["telefone"],
            "email": paciente["email"]
        })

    return jsonify(resultado)


# ==========================================
# EXECUÇÃO DO SISTEMA
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
    