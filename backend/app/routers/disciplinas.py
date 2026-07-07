from fastapi import APIRouter, Request, status
from typing import List
from app.models.disciplina import DisciplinaCadastro, DisciplinaResponse

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

@router.post("/", response_model=DisciplinaResponse, status_code=status.HTTP_201_CREATED, summary="Cadastrar disciplina")
def cadastrar_disciplina(cadastro: DisciplinaCadastro, request: Request):
    """
    Cadastra uma nova disciplina.
    - **codigo**: Código único da disciplina (ex: COMP001)
    - **nome**: Nome da disciplina
    - **ementa**: Descrição da ementa
    - **periodo**: Período sugerido para cursar a disciplina
    """
    return request.app.state.disciplina_service.cadastrar_disciplina(cadastro)

@router.get("/", response_model=List[DisciplinaResponse], summary="Listar disciplinas")
def listar_disciplinas(request: Request):
    """
    Retorna uma lista com todas as disciplinas cadastradas.
    """
    return request.app.state.disciplina_service.listar_disciplinas()
