from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from app.models.enums import TipoPerfil

class Usuario(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    nome: str
    email: EmailStr
    senha: str
    perfil: TipoPerfil
    ativo: bool = True
