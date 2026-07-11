from uuid import uuid4

from app.business.relatorio_acesso_usuarios import (
    EstatisticasAcessoUsuarios,
    RelatorioAcessoUsuariosHTML,
)
from app.main import app
from app.models.enums import TipoPerfil
from app.models.usuario import Discente, Docente, Monitor


def test_calcular_estatisticas_de_acesso_por_status_e_perfil():
    usuarios = [
        Discente(
            id=uuid4(),
            nome="Aluno Ativo",
            login="alunoativo",
            email="aluno.ativo@discente.ufpb.br",
            senha="Password123!",
            perfil=TipoPerfil.DISCENTE,
            ativo=True,
            matricula="2023000001",
        ),
        Docente(
            id=uuid4(),
            nome="Docente Inativo",
            login="docente",
            email="docente@ufpb.br",
            senha="Password123!",
            perfil=TipoPerfil.DOCENTE,
            ativo=False,
        ),
        Monitor(
            id=uuid4(),
            nome="Monitor Ativo",
            login="monitor",
            email="monitor@discente.ufpb.br",
            senha="Password123!",
            perfil=TipoPerfil.MONITOR,
            ativo=True,
            matricula="2023000002",
            cargaHoraria=12,
            disciplinaVinculada="MPS",
        ),
    ]

    estatisticas = EstatisticasAcessoUsuarios.calcular(usuarios)

    assert estatisticas.total_usuarios == 3
    assert estatisticas.usuarios_ativos == 2
    assert estatisticas.usuarios_inativos == 1
    assert estatisticas.percentual_ativos == 66.66666666666666
    assert estatisticas.usuarios_por_perfil == {
        "DISCENTE": 1,
        "DOCENTE": 1,
        "MONITOR": 1,
    }


def test_relatorio_html_usa_template_method_para_montar_documento():
    usuarios = [
        Discente(
            id=uuid4(),
            nome="Aluno",
            login="aluno",
            email="aluno@discente.ufpb.br",
            senha="Password123!",
            perfil=TipoPerfil.DISCENTE,
            ativo=True,
            matricula="2023000001",
        )
    ]

    html = RelatorioAcessoUsuariosHTML().gerar(usuarios)

    assert html.startswith("<!DOCTYPE html>")
    assert "<h1>Relat&oacute;rio de acesso dos usu&aacute;rios</h1>" in html
    assert "<dt>Total de usu&aacute;rios</dt><dd>1</dd>" in html
    assert "<dt>Usu&aacute;rios ativos</dt><dd>1</dd>" in html
    assert "<tr><td>DISCENTE</td><td>1</td></tr>" in html


def test_endpoint_retorna_relatorio_html_de_acesso(client):
    repo = app.state.usuario_service._repo
    repo.add(
        Discente(
            id=uuid4(),
            nome="Aluno",
            login="aluno",
            email="aluno@discente.ufpb.br",
            senha="Password123!",
            perfil=TipoPerfil.DISCENTE,
            ativo=True,
            matricula="2023000001",
        )
    )
    repo.add(
        Docente(
            id=uuid4(),
            nome="Docente",
            login="docente",
            email="docente@ufpb.br",
            senha="Password123!",
            perfil=TipoPerfil.DOCENTE,
            ativo=False,
        )
    )

    response = client.get("/relatorios/acessos/usuarios.html")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "<dt>Total de usu&aacute;rios</dt><dd>2</dd>" in response.text
    assert "<dt>Usu&aacute;rios ativos</dt><dd>1</dd>" in response.text
    assert "<dt>Usu&aacute;rios inativos</dt><dd>1</dd>" in response.text
    assert "<tr><td>DISCENTE</td><td>1</td></tr>" in response.text
    assert "<tr><td>DOCENTE</td><td>1</td></tr>" in response.text
