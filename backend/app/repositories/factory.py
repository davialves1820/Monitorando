"""
Factory de repositórios — ponto único de chaveamento RAM ↔ SQLite.

Lê a variável de ambiente REPO_BACKEND no momento da chamada:
  - "ram"    → implementações InMemory (sem I/O de disco)
  - "sqlite" → implementações SQLite   (padrão de produção)

Uso em main.py (lifespan):
    from app.repositories.factory import make_disciplina_repository, make_usuario_repository
    disciplina_repo = make_disciplina_repository()
    usuario_repo    = make_usuario_repository()
"""

import os

from app.repositories.abstract_disciplina_repository import AbstractDisciplinaRepository
from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository


def make_disciplina_repository() -> AbstractDisciplinaRepository:
    """Instancia e retorna o repositório de disciplinas conforme REPO_BACKEND."""
    backend = os.environ.get("REPO_BACKEND", "sqlite").lower()
    if backend == "ram":
        from app.repositories.in_memory_disciplina_repository import InMemoryDisciplinaRepository
        return InMemoryDisciplinaRepository()
    from app.repositories.disciplina_repository import SQLiteDisciplinaRepository
    return SQLiteDisciplinaRepository()


def make_usuario_repository() -> AbstractUsuarioRepository:
    """Instancia e retorna o repositório de usuários conforme REPO_BACKEND."""
    backend = os.environ.get("REPO_BACKEND", "sqlite").lower()
    if backend == "ram":
        from app.repositories.in_memory_usuario_repository import InMemoryUsuarioRepository
        return InMemoryUsuarioRepository()
    from app.repositories.usuario_repository import SQLiteUsuarioRepository
    return SQLiteUsuarioRepository()
