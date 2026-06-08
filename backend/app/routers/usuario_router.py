from fastapi import APIRouter, status
from app.models.enums import TipoPerfil
from app.models.usuario import (
    UsuarioCadastro,
    DiscenteResponse,
    DocenteResponse
)
from app.services.usuario_service import usuario_service

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def cadastrar(cadastro: UsuarioCadastro):
    usuario = usuario_service.cadastrar_usuario(cadastro)
    if usuario.perfil == TipoPerfil.DISCENTE:
        return DiscenteResponse(
            id=usuario.id,
            nome=usuario.nome,
            email=usuario.email,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
            matricula=usuario.matricula,
            curso=usuario.curso,
            periodo=usuario.periodo,
            disciplinasInteresse=usuario.disciplinasInteresse
        )
    else:
        return DocenteResponse(
            id=usuario.id,
            nome=usuario.nome,
            email=usuario.email,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
            siape=usuario.siape,
            departamento=usuario.departamento,
            isCoordenador=usuario.isCoordenador,
            disciplinas=usuario.disciplinas
        )
