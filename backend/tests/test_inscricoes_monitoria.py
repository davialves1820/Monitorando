import pytest
from fastapi.testclient import TestClient

from app.controllers.facade_singleton_controller import FacadeSingletonController
from app.main import app
from app.repositories.disciplina_repository import disciplina_repository
from app.repositories.inscricao_monitoria_repository import inscricao_monitoria_repository
from app.repositories.usuario_repository import usuario_repository

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_banco():
    inscricao_monitoria_repository.clear()
    disciplina_repository.clear()
    usuario_repository.clear()
    yield
    inscricao_monitoria_repository.clear()
    disciplina_repository.clear()
    usuario_repository.clear()


def _criar_usuario():
    response = client.post("/usuarios", json={
        "nome": "Ana Silva",
        "login": "anasilva",
        "email": "ana.silva@discente.ufpb.br",
        "senha": "Password123!",
        "matricula": "2023001111",
        "curso": "Ciencia da Computacao",
        "periodo": 4,
    })
    assert response.status_code == 201, response.json()
    return response.json()


def _criar_disciplina():
    response = client.post("/disciplinas/", json={
        "codigo": "MPS001",
        "nome": "Metodos de Projeto de Software",
        "ementa": "Processos, arquitetura e padroes de projeto.",
        "periodo": 5,
    })
    assert response.status_code == 201, response.json()
    return response.json()


def _criar_inscricao():
    usuario = _criar_usuario()
    disciplina = _criar_disciplina()
    response = client.post("/inscricoes-monitoria/", json={
        "usuario_id": usuario["id"],
        "disciplina_id": disciplina["id"],
        "motivacao": "Tenho interesse em apoiar a turma na disciplina.",
    })
    assert response.status_code == 201, response.json()
    return response.json(), usuario, disciplina


def test_criar_inscricao_monitoria_com_relacionamentos():
    inscricao, usuario, disciplina = _criar_inscricao()

    assert inscricao["usuario_id"] == usuario["id"]
    assert inscricao["disciplina_id"] == disciplina["id"]
    assert inscricao["motivacao"] == "Tenho interesse em apoiar a turma na disciplina."
    assert inscricao["status"] == "PENDENTE"


def test_listar_e_detalhar_inscricao_monitoria():
    inscricao, _, _ = _criar_inscricao()

    listagem = client.get("/inscricoes-monitoria/")
    assert listagem.status_code == 200
    assert len(listagem.json()) == 1
    assert listagem.json()[0]["id"] == inscricao["id"]

    detalhe = client.get(f"/inscricoes-monitoria/{inscricao['id']}")
    assert detalhe.status_code == 200
    assert detalhe.json()["id"] == inscricao["id"]


def test_atualizar_inscricao_monitoria():
    inscricao, usuario, disciplina = _criar_inscricao()

    response = client.put(f"/inscricoes-monitoria/{inscricao['id']}", json={
        "usuario_id": usuario["id"],
        "disciplina_id": disciplina["id"],
        "motivacao": "Atualizei minha motivacao para a monitoria.",
        "status": "APROVADA",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["motivacao"] == "Atualizei minha motivacao para a monitoria."
    assert data["status"] == "APROVADA"


def test_remover_inscricao_monitoria():
    inscricao, _, _ = _criar_inscricao()

    response = client.delete(f"/inscricoes-monitoria/{inscricao['id']}")
    assert response.status_code == 204

    detalhe = client.get(f"/inscricoes-monitoria/{inscricao['id']}")
    assert detalhe.status_code == 404


def test_criar_inscricao_rejeita_usuario_inexistente():
    disciplina = _criar_disciplina()

    response = client.post("/inscricoes-monitoria/", json={
        "usuario_id": "00000000-0000-0000-0000-000000000001",
        "disciplina_id": disciplina["id"],
        "motivacao": "Quero participar.",
    })

    assert response.status_code == 404
    assert "Usuario" in response.json()["detail"]


def test_facade_singleton_controller_retorna_quantidade_total_de_entidades():
    _criar_inscricao()

    assert FacadeSingletonController() is FacadeSingletonController()

    response = client.get("/facade/quantidade-entidades")
    assert response.status_code == 200
    assert response.json()["quantidade"] == 3
