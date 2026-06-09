from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Disciplina(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    codigo: str
    nome: str
    ementa: str
    periodo: int

# Schemas de Entrada (Request Body)
class DisciplinaCadastro(BaseModel):
    codigo: str
    nome: str
    ementa: str
    periodo: int

# Schemas de Saída (Response Body)
class DisciplinaResponse(BaseModel):
    id: UUID
    codigo: str
    nome: str
    ementa: str
    periodo: int
