"""
Pacote repositories — expõe as interfaces públicas da camada de persistência.

Importar daqui garante que o código externo trabalhe sempre com
as abstrações, nunca com implementações concretas:

    from app.repositories import (
        AbstractUsuarioRepository,
        AbstractDisciplinaRepository,
        AbstractInscricaoMonitoriaRepository,
        AbstractRepositoryFactory,
        get_repository_factory,
    )
"""

from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository
from app.repositories.abstract_disciplina_repository import AbstractDisciplinaRepository
from app.repositories.abstract_inscricao_monitoria_repository import AbstractInscricaoMonitoriaRepository
from app.repositories.abstract_repository_factory import AbstractRepositoryFactory
from app.repositories.factory import get_repository_factory

__all__ = [
    "AbstractUsuarioRepository",
    "AbstractDisciplinaRepository",
    "AbstractInscricaoMonitoriaRepository",
    "AbstractRepositoryFactory",
    "get_repository_factory",
]
