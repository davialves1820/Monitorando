# pyrefly: ignore [missing-import]
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.usuario_repository import usuario_repository
from app.models.usuario import Discente, Docente
from app.models.enums import TipoPerfil
from uuid import uuid4

client = TestClient(app)


# ---------------------------------------------------------------------------
# Fixture: isola cada teste limpando o repositório em memória
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def clear_repository():
    usuario_repository._usuarios.clear()
    yield
    usuario_repository._usuarios.clear()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
DISCENTE_PAYLOAD = {
    "nome": "João Silva",
    "email": "joao.silva@discente.ufpb.br",
    "senha": "Password123",
    "matricula": "2023001234",
    "curso": "Engenharia de Computação",
    "periodo": 3,
}

DOCENTE_PAYLOAD = {
    "nome": "Maria Souza",
    "email": "maria.souza@ufpb.br",
    "senha": "DocentePass1",
    "siape": "1122334",
    "departamento": "Departamento de Informática",
    "isCoordenador": True,
}


def _criar_discente(**overrides):
    """Cria um discente via API e retorna o JSON de resposta."""
    payload = {**DISCENTE_PAYLOAD, **overrides}
    res = client.post("/usuarios", json=payload)
    assert res.status_code == 201, res.json()
    return res.json()


def _seed_discentes(quantidade: int, prefixo: str = "Aluno"):
    """Insere `quantidade` discentes diretamente no repositório."""
    for i in range(quantidade):
        usuario_repository.add(
            Discente(
                id=uuid4(),
                nome=f"{prefixo} {i + 1}",
                email=f"aluno{i + 1}@discente.ufpb.br",
                senha="Hash123",
                perfil=TipoPerfil.DISCENTE,
                ativo=True,
                matricula=f"20230{i + 1:05d}",
                curso="Ciência da Computação",
                periodo=i % 8 + 1,
            )
        )


# ===========================================================================
# CADASTRO DE USUÁRIOS (POST /usuarios)
# ===========================================================================

class TestCadastroUsuario:
    def test_criar_discente_com_sucesso(self):
        response = client.post("/usuarios", json=DISCENTE_PAYLOAD)

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

    def test_criar_docente_com_sucesso(self):
        response = client.post("/usuarios", json=DOCENTE_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Maria Souza"
        assert data["email"] == "maria.souza@ufpb.br"
        assert data["perfil"] == "DOCENTE"
        assert data["siape"] == "1122334"
        assert data["departamento"] == "Departamento de Informática"
        assert data["isCoordenador"] is True
        assert data["ativo"] is True
        assert "senha" not in data

    def test_criar_docente_ci_com_sucesso(self):
        payload = {"nome": "Carlos Roberto", "email": "carlos@ci.ufpb.br", "senha": "DocentePass2"}
        response = client.post("/usuarios", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["perfil"] == "DOCENTE"
        assert data["siape"] == ""
        assert data["departamento"] == ""
        assert data["isCoordenador"] is False

    def test_erro_email_nao_institucional(self):
        payload = {**DISCENTE_PAYLOAD, "email": "joao@gmail.com"}
        response = client.post("/usuarios", json=payload)

        assert response.status_code == 400
        assert response.json()["detail"] == "E-mail inválido ou já cadastrado. Utilize seu e-mail institucional."

    def test_erro_senha_curta(self):
        payload = {**DISCENTE_PAYLOAD, "senha": "Pas1"}
        response = client.post("/usuarios", json=payload)

        assert response.status_code == 400
        assert "8 e 100 caracteres" in response.json()["detail"]

    def test_erro_senha_sem_maiuscula(self):
        payload = {**DISCENTE_PAYLOAD, "senha": "password123"}
        response = client.post("/usuarios", json=payload)

        assert response.status_code == 400
        assert "letra maiúscula" in response.json()["detail"]

    def test_erro_senha_sem_numero(self):
        payload = {**DISCENTE_PAYLOAD, "senha": "Password"}
        response = client.post("/usuarios", json=payload)

        assert response.status_code == 400
        assert "número" in response.json()["detail"]

    def test_erro_discente_sem_matricula(self):
        payload = {k: v for k, v in DISCENTE_PAYLOAD.items() if k != "matricula"}
        response = client.post("/usuarios", json=payload)

        assert response.status_code == 400
        assert response.json()["detail"] == "Preencha todos os campos obrigatórios para continuar"

    def test_erro_email_ja_cadastrado(self):
        client.post("/usuarios", json=DISCENTE_PAYLOAD)
        payload2 = {**DISCENTE_PAYLOAD, "nome": "Outro Nome", "matricula": "9999999999"}
        response = client.post("/usuarios", json=payload2)

        assert response.status_code == 400
        assert response.json()["detail"] == "E-mail inválido ou já cadastrado. Utilize seu e-mail institucional."


# ===========================================================================
# LISTAGEM COM PAGINAÇÃO (GET /usuarios) — RF007
# ===========================================================================

class TestListarUsuarios:
    def test_listar_vazio_retorna_lista_vazia(self):
        response = client.get("/usuarios")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["usuarios"] == []
        assert data["pagina"] == 1
        assert data["limite"] == 50

    def test_listar_estrutura_de_resposta(self):
        _seed_discentes(3)
        response = client.get("/usuarios")

        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "pagina" in data
        assert "limite" in data
        assert "usuarios" in data

    def test_paginacao_padrao_50_registros(self):
        _seed_discentes(120)
        response = client.get("/usuarios")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 120
        assert data["pagina"] == 1
        assert data["limite"] == 50
        assert len(data["usuarios"]) == 50

    def test_paginacao_segunda_pagina(self):
        _seed_discentes(120)
        response = client.get("/usuarios?pagina=2&limite=50")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 120
        assert data["pagina"] == 2
        assert len(data["usuarios"]) == 50

    def test_paginacao_ultima_pagina_parcial(self):
        _seed_discentes(35)
        response = client.get("/usuarios?pagina=2&limite=20")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 35
        assert len(data["usuarios"]) == 15  # 35 - 20 = 15 restantes

    def test_limite_customizado(self):
        _seed_discentes(30)
        response = client.get("/usuarios?limite=10")

        assert response.status_code == 200
        data = response.json()
        assert data["limite"] == 10
        assert len(data["usuarios"]) == 10

    def test_limite_maximo_200_respeitado(self):
        _seed_discentes(250)
        response = client.get("/usuarios?limite=200")

        assert response.status_code == 200
        data = response.json()
        assert len(data["usuarios"]) == 200

    def test_limite_acima_do_maximo_retorna_422(self):
        # FastAPI valida le=200 no Query param e rejeita com 422
        response = client.get("/usuarios?limite=201")

        assert response.status_code == 422

    def test_pagina_invalida_retorna_422(self):
        response = client.get("/usuarios?pagina=0")

        assert response.status_code == 422

    def test_senha_nunca_exposta_na_listagem(self):
        _seed_discentes(1)
        response = client.get("/usuarios")

        assert response.status_code == 200
        for usuario in response.json()["usuarios"]:
            assert "senha" not in usuario


# ===========================================================================
# DETALHE POR ID (GET /usuarios/{id})
# ===========================================================================

class TestDetalharUsuario:
    def test_detalhar_discente_com_sucesso(self):
        criado = _criar_discente()
        usuario_id = criado["id"]

        response = client.get(f"/usuarios/{usuario_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == usuario_id
        assert data["nome"] == DISCENTE_PAYLOAD["nome"]
        assert data["email"] == DISCENTE_PAYLOAD["email"]
        assert data["perfil"] == "DISCENTE"
        assert data["matricula"] == DISCENTE_PAYLOAD["matricula"]
        assert "senha" not in data

    def test_detalhar_docente_com_sucesso(self):
        criado = client.post("/usuarios", json=DOCENTE_PAYLOAD).json()
        usuario_id = criado["id"]

        response = client.get(f"/usuarios/{usuario_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == usuario_id
        assert data["perfil"] == "DOCENTE"
        assert data["siape"] == DOCENTE_PAYLOAD["siape"]
        assert "senha" not in data

    def test_detalhar_id_inexistente_retorna_404(self):
        id_fake = str(uuid4())
        response = client.get(f"/usuarios/{id_fake}")

        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]

    def test_detalhar_uuid_invalido_retorna_422(self):
        response = client.get("/usuarios/nao-e-um-uuid-valido")

        assert response.status_code == 422


# ===========================================================================
# FILTROS (GET /usuarios?nome=...&matricula=...) — RF008
# ===========================================================================

class TestFiltrarUsuarios:
    def _seed_mix(self):
        """Insere 3 discentes e 1 docente com nomes e matrículas conhecidos."""
        usuario_repository.add(Discente(
            id=uuid4(), nome="Ana Paula", email="ana@discente.ufpb.br",
            senha="Hash1", perfil=TipoPerfil.DISCENTE, ativo=True,
            matricula="2023000001", curso="CC", periodo=1,
        ))
        usuario_repository.add(Discente(
            id=uuid4(), nome="Ana Beatriz", email="anab@discente.ufpb.br",
            senha="Hash2", perfil=TipoPerfil.DISCENTE, ativo=True,
            matricula="2023000002", curso="SI", periodo=2,
        ))
        usuario_repository.add(Discente(
            id=uuid4(), nome="Carlos Eduardo", email="carlos@discente.ufpb.br",
            senha="Hash3", perfil=TipoPerfil.DISCENTE, ativo=True,
            matricula="2023000003", curso="EC", periodo=3,
        ))
        usuario_repository.add(Docente(
            id=uuid4(), nome="Ana Professora", email="ana.prof@ufpb.br",
            senha="Hash4", perfil=TipoPerfil.DOCENTE, ativo=True,
        ))

    # --- Filtro por nome ---

    def test_filtro_nome_parcial_retorna_correspondencias(self):
        self._seed_mix()
        response = client.get("/usuarios?nome=Ana")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3  # Ana Paula, Ana Beatriz, Ana Professora
        nomes = [u["nome"] for u in data["usuarios"]]
        assert all("Ana" in n for n in nomes)

    def test_filtro_nome_case_insensitive(self):
        self._seed_mix()
        response = client.get("/usuarios?nome=ana")

        assert response.status_code == 200
        assert response.json()["total"] == 3

    def test_filtro_nome_sem_resultado_retorna_404(self):
        self._seed_mix()
        response = client.get("/usuarios?nome=Inexistente")

        assert response.status_code == 404
        assert "Inexistente" in response.json()["detail"]

    def test_filtro_nome_retorna_somente_correspondencias(self):
        self._seed_mix()
        response = client.get("/usuarios?nome=Carlos")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["usuarios"][0]["nome"] == "Carlos Eduardo"

    # --- Filtro por matrícula ---

    def test_filtro_matricula_exata_retorna_discente(self):
        self._seed_mix()
        response = client.get("/usuarios?matricula=2023000001")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["usuarios"][0]["nome"] == "Ana Paula"

    def test_filtro_matricula_inexistente_retorna_404(self):
        self._seed_mix()
        response = client.get("/usuarios?matricula=9999999999")

        assert response.status_code == 404
        assert "9999999999" in response.json()["detail"]

    def test_filtro_matricula_nao_corresponde_a_docente(self):
        """Docentes não têm matrícula — qualquer busca por matrícula não deve retorná-los."""
        self._seed_mix()
        # Nenhum docente tem matrícula, então qualquer valor deve resultar em 404
        # a menos que algum discente tenha essa matrícula
        response = client.get("/usuarios?matricula=0000000000")

        assert response.status_code == 404

    # --- Filtros combinados ---

    def test_filtro_nome_e_matricula_combinados(self):
        self._seed_mix()
        response = client.get("/usuarios?nome=Ana&matricula=2023000002")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["usuarios"][0]["nome"] == "Ana Beatriz"

    def test_filtro_nome_e_matricula_sem_resultado_retorna_404(self):
        self._seed_mix()
        # Nome existe, mas matrícula não corresponde ao mesmo usuário
        response = client.get("/usuarios?nome=Carlos&matricula=2023000001")

        assert response.status_code == 404
        detail = response.json()["detail"]
        assert "Carlos" in detail
        assert "2023000001" in detail

    # --- Filtros com paginação ---

    def test_filtro_nome_com_paginacao(self):
        # Insere 15 discentes com "Teste" no nome
        for i in range(15):
            usuario_repository.add(Discente(
                id=uuid4(), nome=f"Teste Usuario {i + 1}",
                email=f"teste{i + 1}@discente.ufpb.br",
                senha="Hash1", perfil=TipoPerfil.DISCENTE, ativo=True,
                matricula=f"2024{i + 1:06d}",
            ))

        response = client.get("/usuarios?nome=Teste&pagina=1&limite=10")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert len(data["usuarios"]) == 10
        assert data["pagina"] == 1

    def test_filtro_nome_segunda_pagina(self):
        for i in range(15):
            usuario_repository.add(Discente(
                id=uuid4(), nome=f"Teste Usuario {i + 1}",
                email=f"teste{i + 1}@discente.ufpb.br",
                senha="Hash1", perfil=TipoPerfil.DISCENTE, ativo=True,
                matricula=f"2024{i + 1:06d}",
            ))

        response = client.get("/usuarios?nome=Teste&pagina=2&limite=10")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert len(data["usuarios"]) == 5  # 15 - 10 = 5 restantes
