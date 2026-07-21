from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from app.business.memento.inscricao_monitoria_memento import InscricaoMonitoriaMemento


class InscricaoMonitoria(BaseModel):
    """Originator do padrao Memento: sabe criar e restaurar seu proprio estado."""

    id: UUID = Field(default_factory=uuid4)
    usuario_id: UUID
    disciplina_id: UUID
    motivacao: str
    status: str = "PENDENTE"

    def criar_memento(self) -> InscricaoMonitoriaMemento:
        return InscricaoMonitoriaMemento(
            id=self.id,
            usuario_id=self.usuario_id,
            disciplina_id=self.disciplina_id,
            motivacao=self.motivacao,
            status=self.status,
        )

    @staticmethod
    def restaurar_memento(memento: InscricaoMonitoriaMemento) -> "InscricaoMonitoria":
        return InscricaoMonitoria(
            id=memento.id,
            usuario_id=memento.usuario_id,
            disciplina_id=memento.disciplina_id,
            motivacao=memento.motivacao,
            status=memento.status,
        )


class InscricaoMonitoriaCadastro(BaseModel):
    usuario_id: UUID
    disciplina_id: UUID
    motivacao: str


class InscricaoMonitoriaAtualizacao(BaseModel):
    usuario_id: UUID
    disciplina_id: UUID
    motivacao: str
    status: str = "PENDENTE"


class InscricaoMonitoriaResponse(BaseModel):
    id: UUID
    usuario_id: UUID
    disciplina_id: UUID
    motivacao: str
    status: str
