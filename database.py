import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "clinica.db"


def conectar_banco():
    """Abre a conexão com o banco de dados da clínica."""
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row

    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def criar_tabelas():
    """Cria as tabelas necessárias para o funcionamento do sistema."""

    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            procedimento TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Agendada',

            FOREIGN KEY (paciente_id)
            REFERENCES pacientes(id)
            ON DELETE CASCADE
        )
    """)

    conexao.commit()
    conexao.close()