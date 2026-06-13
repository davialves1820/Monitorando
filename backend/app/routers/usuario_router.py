from fastapi import APIRouter, status, Query, Path, Header, HTTPException
from uuid import UUID
from typing import Optional
from app.models.enums import TipoPerfil
from app.models.usuario import (
    UsuarioCadastro,
    DiscenteResponse,
    DocenteResponse,
    PaginatedUsuarios,
    PromoverRequest,
    MonitorResponse,
    LoginRequest
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
            login=usuario.login,
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
            login=usuario.login,
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
    if usuario.perfil == TipoPerfil.MONITOR:
        return MonitorResponse(
            id=usuario.id,
            nome=usuario.nome,
            login=usuario.login,
            email=usuario.email,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
            matricula=usuario.matricula,
            curso=usuario.curso,
            periodo=usuario.periodo,
            disciplinasInteresse=usuario.disciplinasInteresse,
            cargaHoraria=usuario.cargaHoraria,
            disponivel=usuario.disponivel,
            disciplinaVinculada=usuario.disciplinaVinculada,
        )
    elif usuario.perfil == TipoPerfil.DISCENTE:
        return DiscenteResponse(
            id=usuario.id,
            nome=usuario.nome,
            login=usuario.login,
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
            login=usuario.login,
            email=usuario.email,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
            siape=usuario.siape,
            departamento=usuario.departamento,
            isCoordenador=usuario.isCoordenador,
            disciplinas=usuario.disciplinas,
        )

@router.patch("/{id}/promover", response_model=MonitorResponse, summary="Promover Aluno para Monitor")
def promover_usuario(
    id: UUID = Path(description="ID (UUID) do aluno a ser promovido"),
    request: PromoverRequest = None,
    x_perfil: Optional[str] = Header(None, alias="X-Perfil")
):
    if x_perfil != "COORDENADOR":
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: apenas coordenadores podem realizar esta ação."
        )
    if not request:
        raise HTTPException(
            status_code=400,
            detail="Corpo da requisição é obrigatório."
        )
    usuario_promovido = usuario_service.promover_usuario(id, request)
    return MonitorResponse(
        id=usuario_promovido.id,
        nome=usuario_promovido.nome,
        login=usuario_promovido.login,
        email=usuario_promovido.email,
        perfil=usuario_promovido.perfil,
        ativo=usuario_promovido.ativo,
        matricula=usuario_promovido.matricula,
        curso=usuario_promovido.curso,
        periodo=usuario_promovido.periodo,
        disciplinasInteresse=usuario_promovido.disciplinasInteresse,
        cargaHoraria=usuario_promovido.cargaHoraria,
        disponivel=usuario_promovido.disponivel,
        disciplinaVinculada=usuario_promovido.disciplinaVinculada
    )

@router.patch("/{id}/revogar", response_model=DiscenteResponse, summary="Revogar Monitor para Aluno")
def revogar_monitor(
    id: UUID = Path(description="ID (UUID) do monitor a ser revogado"),
    x_perfil: Optional[str] = Header(None, alias="X-Perfil")
):
    if x_perfil != "COORDENADOR":
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: apenas coordenadores podem realizar esta ação."
        )
    usuario_revogado = usuario_service.revogar_monitor(id)
    return DiscenteResponse(
        id=usuario_revogado.id,
        nome=usuario_revogado.nome,
        login=usuario_revogado.login,
        email=usuario_revogado.email,
        perfil=usuario_revogado.perfil,
        ativo=usuario_revogado.ativo,
        matricula=usuario_revogado.matricula,
        curso=usuario_revogado.curso,
        periodo=usuario_revogado.periodo,
        disciplinasInteresse=usuario_revogado.disciplinasInteresse
    )

@router.post("/login", status_code=status.HTTP_200_OK, summary="Realizar login do usuário")
def login(login_data: LoginRequest):
    usuario = usuario_service.login_usuario(login_data.login, login_data.senha)
    if usuario.perfil == TipoPerfil.MONITOR:
        return MonitorResponse(
            id=usuario.id,
            nome=usuario.nome,
            login=usuario.login,
            email=usuario.email,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
            matricula=usuario.matricula,
            curso=usuario.curso,
            periodo=usuario.periodo,
            disciplinasInteresse=usuario.disciplinasInteresse,
            cargaHoraria=usuario.cargaHoraria,
            disponivel=usuario.disponivel,
            disciplinaVinculada=usuario.disciplinaVinculada,
        )
    elif usuario.perfil == TipoPerfil.DISCENTE:
        return DiscenteResponse(
            id=usuario.id,
            nome=usuario.nome,
            login=usuario.login,
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
            login=usuario.login,
            email=usuario.email,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
            siape=usuario.siape,
            departamento=usuario.departamento,
            isCoordenador=usuario.isCoordenador,
            disciplinas=usuario.disciplinas,
        )
