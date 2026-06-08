from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuario_router
from app.repositories.usuario_repository import usuario_repository
from app.models.usuario import Usuario
from app.models.enums import TipoPerfil

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Popula o repositório em memória na inicialização
    if not usuario_repository.find_all():
        for i in range(120):
            usuario_repository.add(
                Usuario(
                    id=uuid4(),
                    nome=f"Usuario {i + 1}",
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

app.include_router(usuario_router)

@app.get("/")
def root():
    return {"message": "Monitorando API está rodando!"}
