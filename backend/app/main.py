from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuario_router
from app.routers.disciplinas import router as disciplinas_router
from app.repositories.usuario_repository import usuario_repository
from app.models.usuario import Usuario
from app.models.enums import TipoPerfil
from app.exceptions import LoginException

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Popula o repositório em memória na inicialização
    if not usuario_repository.find_all():
        def index_to_letters(index: int) -> str:
            letters = ""
            while index >= 0:
                letters = chr(97 + (index % 26)) + letters
                index = (index // 26) - 1
            return letters

        for i in range(120):
            usuario_repository.add(
                Usuario(
                    id=uuid4(),
                    nome=f"Usuario {i + 1}",
                    login=f"usuario{index_to_letters(i)}",
                    email=f"usuario{i + 1}@exemplo.com",
                    senha=f"senha_hash_{i + 1}",
                    perfil=TipoPerfil.DISCENTE,
                    ativo=True
                )
            )
        print("INFO:  [Mock Data] 120 usuarios de teste carregados em memoria.")
    yield

app = FastAPI(
    title="Monitorando API",
    description="API do sistema Monitorando",
    version="1.0.0",
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

app.include_router(usuario_router)
app.include_router(disciplinas_router)

@app.get("/")
def root():
    return {"message": "Monitorando API está rodando!"}
