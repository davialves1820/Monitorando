import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.usuario_repository import usuario_repository

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_repository():
    # Limpa o repositório em memória antes de cada teste para garantir independência
    usuario_repository._usuarios.clear()

def test_criar_discente_com_sucesso():
    payload = {
        "nome": "João Silva",
        "email": "joao.silva@discente.ufpb.br",
        "senha": "Password123",
        "matricula": "2023001234",
        "curso": "Engenharia de Computação",
        "periodo": 3
    }
    response = client.post("/usuarios", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["nome"] == "João Silva"
    assert data["email"] == "joao.silva@discente.ufpb.br"
    assert data["perfil"] == "DISCENTE"
    assert data["matricula"] == "2023001234"
    assert data["curso"] == "Engenharia de Computação"
    assert data["periodo"] == 3
    assert data["ativo"] is True
    assert "senha" not in data

def test_criar_docente_com_sucesso():
    payload = {
        "nome": "Maria Souza",
        "email": "maria.souza@ufpb.br",
        "senha": "DocentePass1",
        "siape": "1122334",
        "departamento": "Departamento de Informática",
        "isCoordenador": True
    }
    response = client.post("/usuarios", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["nome"] == "Maria Souza"
    assert data["email"] == "maria.souza@ufpb.br"
    assert data["perfil"] == "DOCENTE"
    assert data["siape"] == "1122334"
    assert data["departamento"] == "Departamento de Informática"
    assert data["isCoordenador"] is True
    assert data["ativo"] is True
    assert "senha" not in data

def test_criar_docente_ci_com_sucesso():
    payload = {
        "nome": "Carlos Roberto",
        "email": "carlos@ci.ufpb.br",
        "senha": "DocentePass2"
    }
    response = client.post("/usuarios", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["perfil"] == "DOCENTE"
    assert data["siape"] == ""
    assert data["departamento"] == ""
    assert data["isCoordenador"] is False

def test_erro_email_nao_institucional():
    payload = {
        "nome": "João Silva",
        "email": "joao.silva@gmail.com",
        "senha": "Password123",
        "matricula": "2023001234"
    }
    response = client.post("/usuarios", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "E-mail inválido ou já cadastrado. Utilize seu e-mail institucional."

def test_erro_senha_curta():
    payload = {
        "nome": "João Silva",
        "email": "joao@discente.ufpb.br",
        "senha": "Pas1",
        "matricula": "2023001234"
    }
    response = client.post("/usuarios", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "A senha deve conter entre 8 e 100 caracteres, incluindo pelo menos uma letra maiúscula e um número."

def test_erro_senha_sem_maiuscula():
    payload = {
        "nome": "João Silva",
        "email": "joao@discente.ufpb.br",
        "senha": "password123",
        "matricula": "2023001234"
    }
    response = client.post("/usuarios", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "A senha deve conter entre 8 e 100 caracteres, incluindo pelo menos uma letra maiúscula e um número."

def test_erro_senha_sem_numero():
    payload = {
        "nome": "João Silva",
        "email": "joao@discente.ufpb.br",
        "senha": "Password",
        "matricula": "2023001234"
    }
    response = client.post("/usuarios", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "A senha deve conter entre 8 e 100 caracteres, incluindo pelo menos uma letra maiúscula e um número."

def test_erro_discente_sem_matricula():
    payload = {
        "nome": "João Silva",
        "email": "joao@discente.ufpb.br",
        "senha": "Password123"
    }
    response = client.post("/usuarios", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Preencha todos os campos obrigatórios para continuar"

def test_erro_email_ja_cadastrado():
    payload1 = {
        "nome": "João Silva",
        "email": "joao@discente.ufpb.br",
        "senha": "Password123",
        "matricula": "2023001234"
    }
    payload2 = {
        "nome": "João Outro",
        "email": "joao@discente.ufpb.br",
        "senha": "Password1234",
        "matricula": "2023001235"
    }
    # Primeiro cadastro com sucesso
    res1 = client.post("/usuarios", json=payload1)
    assert res1.status_code == 201
    
    # Segundo cadastro com e-mail duplicado deve falhar
    res2 = client.post("/usuarios", json=payload2)
    assert res2.status_code == 400
    assert res2.json()["detail"] == "E-mail inválido ou já cadastrado. Utilize seu e-mail institucional."
