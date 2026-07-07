from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class InscricaoMonitoria(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    usuario_id: UUID
    disciplina_id: UUID
    motivacao: str
    status: str = "PENDENTE"


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
