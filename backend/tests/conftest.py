"""
Configuração global de testes (pytest conftest).

Estratégia de isolamento:
- Define REPO_BACKEND=ram ANTES de importar qualquer módulo da app.
  Os repositórios InMemory não fazem I/O de disco — cada teste parte de
  um estado limpo sem necessidade de limpar arquivo .db.
- A fixture `reset_repositorios` (autouse) reseta o store entre os testes
  chamando .clear() diretamente nos repositórios injetados via app.state.
"""

import os

# Define o backend RAM ANTES de importar qualquer módulo da app,
# pois factory.py lê REPO_BACKEND no momento da chamada.
os.environ["REPO_BACKEND"] = "ram"

import pytest  # noqa: E402 — import após setenv é intencional
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    """Cliente HTTP de testes reutilizado por toda a sessão."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_repositorios(client):
    """
    Limpa os stores InMemory antes e após cada teste.
    Garante isolamento total sem tocar em disco.
    """
    app.state.disciplina_service._repo.clear()
    app.state.usuario_service._repo.clear()
    yield
    app.state.disciplina_service._repo.clear()
    app.state.usuario_service._repo.clear()
