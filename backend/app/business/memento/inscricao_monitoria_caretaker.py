"""
Caretaker (padrao Memento) responsavel por guardar os mementos das
inscricoes de monitoria.

So mantem o estado imediatamente anterior a ultima atualizacao de cada
inscricao (um memento por id) — suficiente para desfazer apenas a ultima
atualizacao, sem historico completo de undo.
"""

from typing import Dict, Optional
from uuid import UUID

from app.business.memento.inscricao_monitoria_memento import InscricaoMonitoriaMemento


class InscricaoMonitoriaCaretaker:

    def __init__(self) -> None:
        self._ultimo_estado: Dict[UUID, InscricaoMonitoriaMemento] = {}

    def salvar(self, memento: InscricaoMonitoriaMemento) -> None:
        self._ultimo_estado[memento.id] = memento

    def obter(self, id: UUID) -> Optional[InscricaoMonitoriaMemento]:
        return self._ultimo_estado.get(id)

    def descartar(self, id: UUID) -> None:
        self._ultimo_estado.pop(id, None)
