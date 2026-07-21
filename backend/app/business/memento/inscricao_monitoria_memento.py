"""
Memento (padrao GoF) do estado de uma InscricaoMonitoria.

Guarda uma copia imutavel dos atributos da inscricao em um dado instante,
sem expor detalhes internos do Originator (InscricaoMonitoria), permitindo
restaura-la posteriormente.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class InscricaoMonitoriaMemento:
    id: UUID
    usuario_id: UUID
    disciplina_id: UUID
    motivacao: str
    status: str
