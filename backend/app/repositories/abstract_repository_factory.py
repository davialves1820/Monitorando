"""
Factory Method — interface abstrata de criação de repositórios.

Define o contrato que toda factory concreta deve cumprir.
Cada método de fábrica (factory method) retorna uma interface abstrata de
repositório, garantindo que o código cliente (services, main.py) nunca
dependa de uma implementação concreta (DIP + Factory Method GoF).

Implementações concretas:
  - SQLiteRepositoryFactory   → repositórios com persistência em SQLite
  - InMemoryRepositoryFactory → repositórios em RAM (testes / modo efêmero)

Seleção da factory em tempo de execução:
    from app.repositories.factory import get_repository_factory
    factory = get_repository_factory()          # lê REPO_BACKEND do ambiente
    usuario_repo = factory.create_usuario_repository()
"""

from abc import ABC, abstractmethod

from app.repositories.abstract_disciplina_repository import AbstractDisciplinaRepository
from app.repositories.abstract_inscricao_monitoria_repository import AbstractInscricaoMonitoriaRepository
from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository


class AbstractRepositoryFactory(ABC):
    """
    Fábrica abstrata de repositórios (Factory Method / Abstract Factory GoF).

    Cada método é um *factory method* responsável por instanciar e retornar
    a implementação correta do repositório para a entidade correspondente.
    O código chamador trabalha exclusivamente com as interfaces abstratas,
    sem conhecer se o backend é SQLite, RAM ou qualquer outro.
    """

    @abstractmethod
    def create_usuario_repository(self) -> AbstractUsuarioRepository:
        """
        Factory method para o repositório de usuários.

        Returns:
            Uma implementação concreta de AbstractUsuarioRepository.
        """
        ...

    @abstractmethod
    def create_disciplina_repository(self) -> AbstractDisciplinaRepository:
        """
        Factory method para o repositório de disciplinas.

        Returns:
            Uma implementação concreta de AbstractDisciplinaRepository.
        """
        ...

    @abstractmethod
    def create_inscricao_monitoria_repository(self) -> AbstractInscricaoMonitoriaRepository:
        """
        Factory method para o repositório de inscrições de monitoria.

        Returns:
            Uma implementação concreta de AbstractInscricaoMonitoriaRepository.
        """
        ...
