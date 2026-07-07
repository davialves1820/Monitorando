"""
Implementação RAM do repositório de disciplinas.

Armazena dados em um dicionário interno — sem I/O de disco.
Ideal para testes e para subir a aplicação em modo efêmero.

Selecionada quando REPO_BACKEND=ram (ver app/repositories/factory.py).
"""

from typing import Dict, List, Optional
from uuid import UUID

from app.models.disciplina import Disciplina
from app.repositories.abstract_disciplina_repository import AbstractDisciplinaRepository


class InMemoryDisciplinaRepository(AbstractDisciplinaRepository):
    """Repositório de disciplinas com armazenamento em memória RAM."""

    def __init__(self) -> None:
        self._store: Dict[UUID, Disciplina] = {}

    def add(self, disciplina: Disciplina) -> Disciplina:
        self._store[disciplina.id] = disciplina
        return disciplina

    def find_all(self) -> List[Disciplina]:
        return list(self._store.values())

    def find_by_codigo(self, codigo: str) -> Optional[Disciplina]:
        for disciplina in self._store.values():
            if disciplina.codigo == codigo:
                return disciplina
        return None

    def clear(self) -> None:
        self._store.clear()
