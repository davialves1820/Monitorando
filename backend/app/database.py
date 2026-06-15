"""
Módulo de configuração do banco de dados SQLite.

Responsabilidades:
- Definir o caminho do arquivo de banco de dados.
- Criar as tabelas necessárias (schema) caso ainda não existam.
- Fornecer a função `get_connection()` para os repositórios.
"""

import sqlite3
import os
from app.exceptions import DatabaseException

# Caminho padrão do banco de dados. Pode ser sobrescrito em testes via
# variável de ambiente DB_PATH (ver conftest.py).
DB_PATH: str = os.environ.get("DB_PATH", "monitorando.db")


def get_connection() -> sqlite3.Connection:
    """
    Retorna uma conexão com o banco de dados SQLite configurado em DB_PATH.

    Usa `detect_types` para suporte a tipos Python via adaptadores e
    `row_factory = sqlite3.Row` para acesso às colunas por nome.

    Raises:
        DatabaseException: se não for possível abrir a conexão.
    """
    try:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        # Habilita chaves estrangeiras (boa prática mesmo não usadas agora)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.DatabaseError as e:
        raise DatabaseException(f"Não foi possível conectar ao banco de dados: {e}")


def inicializar_banco() -> None:
    """
    Cria as tabelas do sistema caso ainda não existam (idempotente).

    Tabelas criadas:
    - usuarios: armazena todos os perfis (discente, docente, monitor)
      usando uma coluna `tipo` como discriminador de herança.
    - disciplinas: armazena as disciplinas cadastradas.

    Raises:
        DatabaseException: se ocorrer erro de acesso ao banco.
    """
    try:
        with get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id              TEXT PRIMARY KEY,
                    nome            TEXT NOT NULL,
                    login           TEXT NOT NULL UNIQUE,
                    email           TEXT NOT NULL UNIQUE,
                    senha           TEXT NOT NULL,
                    perfil          TEXT NOT NULL,
                    ativo           INTEGER NOT NULL DEFAULT 1,
                    tipo            TEXT NOT NULL,

                    -- Atributos de Discente / Monitor
                    matricula               TEXT,
                    curso                   TEXT,
                    periodo                 INTEGER,
                    disciplinas_interesse   TEXT,

                    -- Atributos de Docente
                    siape                   TEXT,
                    departamento            TEXT,
                    is_coordenador          INTEGER,
                    disciplinas_docente     TEXT,

                    -- Atributos exclusivos de Monitor
                    carga_horaria           INTEGER,
                    disponivel              INTEGER,
                    disciplina_vinculada    TEXT
                );

                CREATE TABLE IF NOT EXISTS disciplinas (
                    id      TEXT PRIMARY KEY,
                    codigo  TEXT NOT NULL UNIQUE,
                    nome    TEXT NOT NULL,
                    ementa  TEXT NOT NULL,
                    periodo INTEGER NOT NULL
                );
            """)
    except sqlite3.DatabaseError as e:
        raise DatabaseException(f"Erro ao inicializar o banco de dados: {e}")
