from typing import List, Optional
from uuid import UUID
from app.models.disciplina import Disciplina

class DisciplinaRepository:
    def __init__(self):
        self._disciplinas: List[Disciplina] = []

    def add(self, disciplina: Disciplina) -> Disciplina:
        self._disciplinas.append(disciplina)
        return disciplina

    def find_all(self) -> List[Disciplina]:
        return self._disciplinas

    def find_by_codigo(self, codigo: str) -> Optional[Disciplina]:
        for d in self._disciplinas:
            if d.codigo == codigo:
                return d
        return None

# Instância global para simular o banco de dados em memória
disciplina_repository = DisciplinaRepository()
