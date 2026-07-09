"""
Factory Method — implementação concreta SQLite.

Instancia os repositórios que persistem dados em SQLite.
Selecionada automaticamente quando REPO_BACKEND=sqlite (padrão de produção).

Nunca importe esta classe diretamente no código de negócio.
Use sempre a interface AbstractRepositoryFactory ou a função
get_repository_factory() definida em factory.py.
"""

from app.repositories.abstract_disciplina_repository import AbstractDisciplinaRepository
from app.repositories.abstract_inscricao_monitoria_repository import AbstractInscricaoMonitoriaRepository
from app.repositories.abstract_repository_factory import AbstractRepositoryFactory
from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository


class SQLiteRepositoryFactory(AbstractRepositoryFactory):
    """
    Factory concreta que produz repositórios com backend SQLite.

    Cada factory method faz o import local da classe concreta para evitar
    que dependências de sqlite3 sejam carregadas quando o backend RAM
    é selecionado (lazy import).
    """

    def create_usuario_repository(self) -> AbstractUsuarioRepository:
        """Retorna um SQLiteUsuarioRepository pronto para uso."""
        from app.repositories.usuario_repository import SQLiteUsuarioRepository
        return SQLiteUsuarioRepository()

    def create_disciplina_repository(self) -> AbstractDisciplinaRepository:
        """Retorna um SQLiteDisciplinaRepository pronto para uso."""
        from app.repositories.disciplina_repository import SQLiteDisciplinaRepository
        return SQLiteDisciplinaRepository()

    def create_inscricao_monitoria_repository(self) -> AbstractInscricaoMonitoriaRepository:
        """Retorna um SQLiteInscricaoMonitoriaRepository pronto para uso."""
        from app.repositories.inscricao_monitoria_repository import SQLiteInscricaoMonitoriaRepository
        return SQLiteInscricaoMonitoriaRepository()
