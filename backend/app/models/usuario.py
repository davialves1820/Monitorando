from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from typing import List, Optional
from app.models.enums import TipoPerfil

class Usuario(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    nome: str
    email: EmailStr
    senha: str
    perfil: TipoPerfil
    ativo: bool = True

class Discente(Usuario):
    matricula: str
    curso: str = ""
    periodo: Optional[int] = None
    disciplinasInteresse: List[str] = []

class Docente(Usuario):
    siape: str = ""
    departamento: str = ""
    isCoordenador: bool = False
    disciplinas: List[str] = []

# Schemas de Entrada (Request Body)
class UsuarioCadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    matricula: Optional[str] = None
    curso: Optional[str] = None
    periodo: Optional[int] = None
    siape: Optional[str] = None
    departamento: Optional[str] = None
    isCoordenador: Optional[bool] = False

# Schemas de Saída (Response Body)
class UsuarioResponse(BaseModel):
    id: UUID
    nome: str
    email: EmailStr
    perfil: TipoPerfil
    ativo: bool

class DiscenteResponse(UsuarioResponse):
    matricula: str
    curso: str = ""
    periodo: Optional[int] = None
    disciplinasInteresse: List[str] = []

class DocenteResponse(UsuarioResponse):
    siape: str = ""
    departamento: str = ""
    isCoordenador: bool = False
    disciplinas: List[str] = []

