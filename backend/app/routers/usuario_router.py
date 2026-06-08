from fastapi import APIRouter, status, Query
from app.models.enums import TipoPerfil
from app.models.usuario import (
    UsuarioCadastro,
    DiscenteResponse,
    DocenteResponse,
    PaginatedUsuarios
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


@router.get(
    "",
    response_model=PaginatedUsuarios,
    summary="Listar usuários",
    description=(
        "Retorna todos os usuários cadastrados com paginação. "
        "Limite padrão: 50 registros por página (RF007). "
        "Máximo permitido: 200 registros por página."
    ),
)
def listar_usuarios(
    pagina: int = Query(default=1, ge=1, description="Número da página (começa em 1)"),
    limite: int = Query(default=50, ge=1, le=200, description="Quantidade de registros por página (padrão: 50)"),
) -> PaginatedUsuarios:
    return usuario_service.listar_usuarios(pagina=pagina, limite=limite)
