import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_disciplina_com_sucesso():
    payload = {
        "codigo": "COMP001",
        "nome": "Introdução à Programação",
        "ementa": "Lógica de programação, variáveis, laços de repetição e funções.",
        "periodo": 1
    }
    
    response = client.post("/disciplinas/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["codigo"] == "COMP001"
    assert "id" in data

def test_criar_disciplina_codigo_duplicado():
    # Cria a primeira vez (pode falhar se o BD não for resetado, mas como está em memória, a ordem do Pytest importa)
    # Por segurança, vamos usar um código diferente
    payload = {
        "codigo": "COMP002",
        "nome": "Estrutura de Dados",
        "ementa": "Listas, pilhas, filas e árvores.",
        "periodo": 3
    }
    client.post("/disciplinas/", json=payload)
    
    # Tenta criar de novo
    response = client.post("/disciplinas/", json=payload)
    assert response.status_code == 400
    assert "Já existe uma disciplina com este código" in response.json()["detail"]

def test_criar_disciplina_dados_invalidos():
    payload = {
        "codigo": "",
        "nome": "Materia Vazia",
        "ementa": "",
        "periodo": 1
    }
    response = client.post("/disciplinas/", json=payload)
    assert response.status_code == 400
    assert "Preencha todos os campos obrigatórios" in response.json()["detail"]

def test_listar_disciplinas():
    response = client.get("/disciplinas/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Deve ter pelo menos as disciplinas criadas nos testes anteriores
    assert len(data) >= 2
