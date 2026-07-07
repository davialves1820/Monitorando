"""
Interface abstrata do repositório de disciplinas.

Qualquer implementação concreta (RAM, SQLite, etc.) deve estender esta classe
e implementar todos os métodos aqui declarados.

Princípio aplicado: DIP — os services dependem desta abstração,
nunca de uma implementação concreta.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.models.disciplina import Disciplina


class AbstractDisciplinaRepository(ABC):

    @abstractmethod
    def add(self, disciplina: Disciplina) -> Disciplina:
        """Persiste uma nova disciplina. Retorna o objeto persistido."""
        ...

    @abstractmethod
    def find_all(self) -> List[Disciplina]:
        """Retorna todas as disciplinas cadastradas."""
        ...

    @abstractmethod
    def find_by_codigo(self, codigo: str) -> Optional[Disciplina]:
        """Busca uma disciplina pelo código (exato, case-sensitive). Retorna None se não encontrada."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove todos os registros (usado em testes para isolamento)."""
        ...
