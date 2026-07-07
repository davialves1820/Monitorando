from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from typing import List, Optional
from app.models.enums import TipoPerfil

class Usuario(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    nome: str
    login: str
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

class Monitor(Discente):
    perfil: TipoPerfil = TipoPerfil.MONITOR
    cargaHoraria: int
    disponivel: bool = True
    disciplinaVinculada: str

# Schemas de Entrada (Request Body)
class UsuarioCadastro(BaseModel):
    nome: str
    login: str
    email: EmailStr
    senha: str
    matricula: Optional[str] = None
    curso: Optional[str] = None
    periodo: Optional[int] = None
    siape: Optional[str] = None
    departamento: Optional[str] = None
    isCoordenador: Optional[bool] = False

class PromoverRequest(BaseModel):
    disciplinaVinculada: str
    cargaHoraria: int = Field(..., ge=0)

class LoginRequest(BaseModel):
    login: str
    senha: str

# Schemas de Saída (Response Body)
class UsuarioResponse(BaseModel):
    id: UUID
    nome: str
    login: str
    email: EmailStr
    perfil: TipoPerfil
    ativo: bool

    @staticmethod
    def from_domain(usuario: "Usuario") -> "UsuarioResponse":
        if usuario.perfil == TipoPerfil.MONITOR:
            return MonitorResponse(
                id=usuario.id,
                nome=usuario.nome,
                login=usuario.login,
                email=usuario.email,
                perfil=usuario.perfil,
                ativo=usuario.ativo,
                matricula=usuario.matricula,
                curso=usuario.curso,
                periodo=usuario.periodo,
                disciplinasInteresse=usuario.disciplinasInteresse,
                cargaHoraria=usuario.cargaHoraria,
                disponivel=usuario.disponivel,
                disciplinaVinculada=usuario.disciplinaVinculada,
            )
        elif usuario.perfil == TipoPerfil.DISCENTE:
            return DiscenteResponse(
                id=usuario.id,
                nome=usuario.nome,
                login=usuario.login,
                email=usuario.email,
                perfil=usuario.perfil,
                ativo=usuario.ativo,
                matricula=usuario.matricula,
                curso=usuario.curso,
                periodo=usuario.periodo,
                disciplinasInteresse=usuario.disciplinasInteresse,
            )
        else:
            return DocenteResponse(
                id=usuario.id,
                nome=usuario.nome,
                login=usuario.login,
                email=usuario.email,
                perfil=usuario.perfil,
                ativo=usuario.ativo,
                siape=usuario.siape,
                departamento=usuario.departamento,
                isCoordenador=usuario.isCoordenador,
                disciplinas=usuario.disciplinas,
            )

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

class MonitorResponse(DiscenteResponse):
    perfil: TipoPerfil = TipoPerfil.MONITOR
    cargaHoraria: int
    disponivel: bool
    disciplinaVinculada: str

class PaginatedUsuarios(BaseModel):
    """Resposta paginada da listagem de usuários (RF007)."""
    total: int
    pagina: int
    limite: int
    usuarios: List[UsuarioResponse]


