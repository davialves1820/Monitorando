"""
Ponto único de chaveamento entre backends de persistência.

Expõe a função get_repository_factory() que lê a variável de ambiente
REPO_BACKEND e retorna a factory concreta correspondente:

  - "ram"    → InMemoryRepositoryFactory  (sem I/O de disco)
  - "sqlite" → SQLiteRepositoryFactory    (padrão de produção)

Padrão aplicado: Factory Method (GoF)
  A decisão de qual implementação concreta usar é centralizada aqui.
  O código chamador (main.py, testes) recebe uma AbstractRepositoryFactory
  e nunca conhece a classe concreta — mantendo o DIP.

Uso recomendado (main.py / lifespan):
    from app.repositories.factory import get_repository_factory

    factory      = get_repository_factory()
    usuario_repo = factory.create_usuario_repository()
    disc_repo    = factory.create_disciplina_repository()
    inscricao_r  = factory.create_inscricao_monitoria_repository()

Funções de conveniência legadas (make_*):
    Mantidas para compatibilidade retroativa — delegam para a factory.
    Prefira usar get_repository_factory() em código novo.
"""

import os

from app.repositories.abstract_repository_factory import AbstractRepositoryFactory
from app.repositories.abstract_disciplina_repository import AbstractDisciplinaRepository
from app.repositories.abstract_inscricao_monitoria_repository import AbstractInscricaoMonitoriaRepository
from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository


def get_repository_factory() -> AbstractRepositoryFactory:
    """
    Retorna a factory de repositórios adequada ao backend configurado.

    Lê a variável de ambiente REPO_BACKEND (default: "sqlite"):
      - "ram"    → InMemoryRepositoryFactory
      - "sqlite" → SQLiteRepositoryFactory

    Returns:
        Uma instância de AbstractRepositoryFactory pronta para criar repositórios.

    Example::

        factory = get_repository_factory()
        repo    = factory.create_usuario_repository()
    """
    backend = os.environ.get("REPO_BACKEND", "sqlite").lower()

    if backend == "ram":
        from app.repositories.in_memory_repository_factory import InMemoryRepositoryFactory
        return InMemoryRepositoryFactory()

    from app.repositories.sqlite_repository_factory import SQLiteRepositoryFactory
    return SQLiteRepositoryFactory()


# ---------------------------------------------------------------------------
# Funções de conveniência (API legada — mantidas para compatibilidade)
# ---------------------------------------------------------------------------

def make_disciplina_repository() -> AbstractDisciplinaRepository:
    """
    Atalho legado — equivalente a get_repository_factory().create_disciplina_repository().

    .. deprecated::
        Prefira obter a factory via get_repository_factory() e chamar o método correspondente.
    """
    return get_repository_factory().create_disciplina_repository()


def make_usuario_repository() -> AbstractUsuarioRepository:
    """
    Atalho legado — equivalente a get_repository_factory().create_usuario_repository().

    .. deprecated::
        Prefira obter a factory via get_repository_factory() e chamar o método correspondente.
    """
    return get_repository_factory().create_usuario_repository()


def make_inscricao_monitoria_repository() -> AbstractInscricaoMonitoriaRepository:
    """
    Atalho legado — equivalente a get_repository_factory().create_inscricao_monitoria_repository().

    .. deprecated::
        Prefira obter a factory via get_repository_factory() e chamar o método correspondente.
    """
    return get_repository_factory().create_inscricao_monitoria_repository()
