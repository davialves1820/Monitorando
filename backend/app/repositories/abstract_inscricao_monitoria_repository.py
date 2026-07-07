"""
Interface abstrata do repositório de inscrições de monitoria.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.models.inscricao_monitoria import InscricaoMonitoria


class AbstractInscricaoMonitoriaRepository(ABC):

    @abstractmethod
    def add(self, inscricao: InscricaoMonitoria) -> InscricaoMonitoria:
        ...

    @abstractmethod
    def find_all(self) -> List[InscricaoMonitoria]:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> Optional[InscricaoMonitoria]:
        ...

    @abstractmethod
    def update(self, inscricao: InscricaoMonitoria) -> Optional[InscricaoMonitoria]:
        ...

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...
