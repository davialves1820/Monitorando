"""
Factory Method — implementação concreta InMemory (RAM).

Instancia os repositórios que armazenam dados em memória — sem I/O de disco.
Selecionada automaticamente quando REPO_BACKEND=ram (testes / modo efêmero).

Nunca importe esta classe diretamente no código de negócio.
Use sempre a interface AbstractRepositoryFactory ou a função
get_repository_factory() definida em factory.py.
"""

from app.repositories.abstract_disciplina_repository import AbstractDisciplinaRepository
from app.repositories.abstract_inscricao_monitoria_repository import AbstractInscricaoMonitoriaRepository
from app.repositories.abstract_repository_factory import AbstractRepositoryFactory
from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository


class InMemoryRepositoryFactory(AbstractRepositoryFactory):
    """
    Factory concreta que produz repositórios com backend em memória RAM.

    Ideal para testes unitários e cenários onde persistência entre reinicializações
    não é necessária. Cada chamada a um factory method retorna uma *nova* instância
    independente — o compartilhamento de estado entre repositories, quando necessário,
    deve ser gerenciado pelo código chamador (ex.: main.py / lifespan).
    """

    def create_usuario_repository(self) -> AbstractUsuarioRepository:
        """Retorna um InMemoryUsuarioRepository pronto para uso."""
        from app.repositories.in_memory_usuario_repository import InMemoryUsuarioRepository
        return InMemoryUsuarioRepository()

    def create_disciplina_repository(self) -> AbstractDisciplinaRepository:
        """Retorna um InMemoryDisciplinaRepository pronto para uso."""
        from app.repositories.in_memory_disciplina_repository import InMemoryDisciplinaRepository
        return InMemoryDisciplinaRepository()

    def create_inscricao_monitoria_repository(self) -> AbstractInscricaoMonitoriaRepository:
        """Retorna um InMemoryInscricaoMonitoriaRepository pronto para uso."""
        from app.repositories.in_memory_inscricao_monitoria_repository import InMemoryInscricaoMonitoriaRepository
        return InMemoryInscricaoMonitoriaRepository()
