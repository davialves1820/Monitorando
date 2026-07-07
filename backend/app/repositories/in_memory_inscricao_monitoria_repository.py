"""
Implementação RAM do repositório de inscrições de monitoria.
"""

from typing import Dict, List, Optional
from uuid import UUID

from app.models.inscricao_monitoria import InscricaoMonitoria
from app.repositories.abstract_inscricao_monitoria_repository import AbstractInscricaoMonitoriaRepository


class InMemoryInscricaoMonitoriaRepository(AbstractInscricaoMonitoriaRepository):

    def __init__(self) -> None:
        self._store: Dict[UUID, InscricaoMonitoria] = {}

    def add(self, inscricao: InscricaoMonitoria) -> InscricaoMonitoria:
        self._store[inscricao.id] = inscricao
        return inscricao

    def find_all(self) -> List[InscricaoMonitoria]:
        return list(self._store.values())

    def find_by_id(self, id: UUID) -> Optional[InscricaoMonitoria]:
        return self._store.get(id)

    def update(self, inscricao: InscricaoMonitoria) -> Optional[InscricaoMonitoria]:
        if inscricao.id not in self._store:
            return None
        self._store[inscricao.id] = inscricao
        return inscricao

    def delete(self, id: UUID) -> bool:
        if id not in self._store:
            return False
        del self._store[id]
        return True

    def count(self) -> int:
        return len(self._store)

    def clear(self) -> None:
        self._store.clear()
