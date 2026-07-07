from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import inicializar_banco
from app.routers import usuario_router
from app.routers.disciplinas import router as disciplinas_router
from app.routers.facade_router import router as facade_router
from app.routers.inscricao_monitoria_router import router as inscricoes_monitoria_router
from app.exceptions import LoginException, IOException, DatabaseException, SenhaException


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Garante que as tabelas existam antes de qualquer requisição
    inicializar_banco()
    print("INFO:  [DB] Banco de dados SQLite inicializado.")
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

@app.exception_handler(IOException)
async def io_exception_handler(request: Request, exc: IOException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message if hasattr(exc, "message") else str(exc)}
    )


@app.exception_handler(DatabaseException)
async def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message if hasattr(exc, "message") else str(exc)}
    )


app.include_router(usuario_router)
app.include_router(disciplinas_router)
app.include_router(inscricoes_monitoria_router)
app.include_router(facade_router)


@app.get("/")
def root():
    return {"message": "Monitorando API está rodando!"}
