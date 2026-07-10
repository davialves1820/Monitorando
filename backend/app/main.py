import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.repositories.factory import (
    make_disciplina_repository,
    make_usuario_repository,
    make_inscricao_monitoria_repository,
)
from app.services.disciplina_service import DisciplinaService
from app.services.usuario_service import UsuarioService
from app.services.inscricao_monitoria_service import InscricaoMonitoriaService
from app.controllers.facade_singleton_controller import facade_singleton_controller
from app.routers import usuario_router
from app.routers.disciplinas import router as disciplinas_router
from app.routers.facade_router import router as facade_router
from app.routers.inscricao_monitoria_router import router as inscricoes_monitoria_router
from app.exceptions import (
    LoginException,
    SenhaException,
    DatabaseException,
    CredenciaisInvalidasException,
    UsuarioNaoEncontradoException,
    InscricaoNaoEncontradaException,
    DisciplinaNaoEncontradaException,
    EmailJaCadastradoException,
    DisciplinaCodigoJaExisteException,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Boot da aplicação: escolhe o backend de persistência via REPO_BACKEND,
    instancia os repositórios e os injeta nos services.

    REPO_BACKEND=sqlite  → persistência em SQLite (padrão de produção)
    REPO_BACKEND=ram     → armazenamento em RAM   (ephemeral / testes)
    """
    backend = os.environ.get("REPO_BACKEND", "sqlite").lower()

    # --- repositórios ---
    disciplina_repo  = make_disciplina_repository()
    usuario_repo     = make_usuario_repository()
    inscricao_repo   = make_inscricao_monitoria_repository()

    # --- services (dependem da interface, não da implementação) ---
    disciplina_svc          = DisciplinaService(repo=disciplina_repo)
    usuario_svc             = UsuarioService(repo=usuario_repo)
    inscricao_monitoria_svc = InscricaoMonitoriaService(
        inscricao_repo=inscricao_repo,
        usuario_repo=usuario_repo,
        disciplina_repo=disciplina_repo,
    )

    app.state.disciplina_service          = disciplina_svc
    app.state.usuario_service             = usuario_svc
    app.state.inscricao_monitoria_service = inscricao_monitoria_svc

    # --- facade singleton (recebe os services via initialize) ---
    facade_singleton_controller.initialize(
        usuario_service=usuario_svc,
        disciplina_service=disciplina_svc,
        inscricao_monitoria_service=inscricao_monitoria_svc,
    )

    # Inicializa o schema do banco apenas quando o backend for SQLite
    if backend == "sqlite":
        from app.database import inicializar_banco
        inicializar_banco()

    print(f"INFO:  [BOOT] REPO_BACKEND={backend.upper()} — repositórios inicializados.")
    yield


app = FastAPI(
    title="Monitorando API",
    description="API do sistema de monitoria acadêmica Monitorando",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(LoginException)
async def login_exception_handler(request: Request, exc: LoginException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message if hasattr(exc, "message") else str(exc)}
    )


@app.exception_handler(SenhaException)
async def senha_exception_handler(request: Request, exc: SenhaException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message if hasattr(exc, "message") else str(exc)}
    )


@app.exception_handler(DatabaseException)
async def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message if hasattr(exc, "message") else str(exc)}
    )


@app.exception_handler(UsuarioNaoEncontradoException)
async def usuario_nao_encontrado_handler(request: Request, exc: UsuarioNaoEncontradoException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(InscricaoNaoEncontradaException)
async def inscricao_nao_encontrada_handler(request: Request, exc: InscricaoNaoEncontradaException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(DisciplinaNaoEncontradaException)
async def disciplina_nao_encontrada_handler(request: Request, exc: DisciplinaNaoEncontradaException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(EmailJaCadastradoException)
async def email_ja_cadastrado_handler(request: Request, exc: EmailJaCadastradoException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )


@app.exception_handler(DisciplinaCodigoJaExisteException)
async def disciplina_codigo_ja_existe_handler(request: Request, exc: DisciplinaCodigoJaExisteException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )


@app.exception_handler(CredenciaisInvalidasException)
async def credenciais_invalidas_handler(request: Request, exc: CredenciaisInvalidasException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
    )


app.include_router(usuario_router)
app.include_router(disciplinas_router)
app.include_router(inscricoes_monitoria_router)
app.include_router(facade_router)


@app.get("/")
def root():
    return {"message": "Monitorando API está rodando!"}
