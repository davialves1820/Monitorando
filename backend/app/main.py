from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuario_router

app = FastAPI(
    title="Monitorando API",
    description="API do sistema Monitorando",
    version="1.0.0"
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

