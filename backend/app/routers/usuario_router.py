from fastapi import APIRouter, status, Query, Path
from uuid import UUID
from typing import Optional
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
    summary="Listar / filtrar usuários",
    description=(
        "Retorna usuários cadastrados com paginação (RF007). "
        "Filtros opcionais: **nome** (busca parcial, case-insensitive) e "
        "**matricula** (busca exata). "
        "Retorna **404** quando nenhum resultado for encontrado com os filtros informados (RF008)."
    ),
    responses={
        200: {"description": "Usuários encontrados"},
        404: {"description": "Nenhum usuário encontrado com os filtros informados"},
    },
)
def listar_usuarios(
    nome: Optional[str] = Query(default=None, description="Filtro por nome (parcial, case-insensitive)"),
    matricula: Optional[str] = Query(default=None, description="Filtro por matrícula (exata, somente discentes)"),
    pagina: int = Query(default=1, ge=1, description="Número da página (começa em 1)"),
    limite: int = Query(default=50, ge=1, le=200, description="Registros por página (padrão: 50)"),
) -> PaginatedUsuarios:
    if nome or matricula:
        return usuario_service.buscar_usuarios(
            nome=nome,
            matricula=matricula,
            pagina=pagina,
            limite=limite,
        )
    return usuario_service.listar_usuarios(pagina=pagina, limite=limite)



@router.get(
    "/{id}",
    summary="Detalhar usuário",
    description="Retorna os dados completos de um usuário específico pelo seu ID (UUID).",
    responses={
        200: {"description": "Usuário encontrado"},
        404: {"description": "Usuário não encontrado"},
    },
)
def detalhar_usuario(
    id: UUID = Path(description="ID (UUID) do usuário a ser consultado"),
):
    usuario = usuario_service.buscar_usuario_por_id(id)
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
            disciplinasInteresse=usuario.disciplinasInteresse,
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
            disciplinas=usuario.disciplinas,
        )
