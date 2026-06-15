"""
Configuração global de testes (pytest conftest).

Estratégia de isolamento de banco de dados:
- Define a variável de ambiente `DB_PATH` apontando para um arquivo
  temporário de testes (`monitorando_test.db`) ANTES de qualquer importação
  dos módulos da aplicação.
- A fixture `reset_banco` (autouse em módulos que a incluem) limpa todas
  as tabelas entre os testes, garantindo isolamento sem recriação do schema.
"""

import os
import sqlite3

# Define o banco de dados de testes ANTES de importar qualquer módulo da app,
# pois `database.py` lê DB_PATH no momento da importação do módulo.
os.environ["DB_PATH"] = "monitorando_test.db"

import pytest  # noqa: E402 — import após setenv é intencional

from app.database import inicializar_banco  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def criar_schema():
    """
    Cria o schema do banco de testes uma única vez por sessão de testes.
    Garante que as tabelas existam antes de qualquer teste rodar.
    """
    inicializar_banco()
    yield
    # Limpeza final: remove o arquivo de banco de testes após a sessão.
    # No Windows, o SQLite pode manter o arquivo aberto brevemente após o
    # último uso — por isso usamos try/except para não falhar o teardown.
    db_path = os.environ.get("DB_PATH", "monitorando_test.db")
    import gc
    import time
    gc.collect()  # força GC para fechar conexões que ainda estão na memória
    time.sleep(0.1)  # aguarda o OS liberar o handle do arquivo
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except PermissionError:
        pass  # arquivo ainda em uso — será limpo no próximo run
