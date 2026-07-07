from fastapi import APIRouter, status
from typing import List
from app.models.disciplina import DisciplinaCadastro, DisciplinaResponse
from app.services.disciplina_service import disciplina_service

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

@router.post("/", response_model=DisciplinaResponse, status_code=status.HTTP_201_CREATED, summary="Cadastrar disciplina")
def cadastrar_disciplina(cadastro: DisciplinaCadastro):
    """
    Cadastra uma nova disciplina.
    - **codigo**: Código único da disciplina (ex: COMP001)
    - **nome**: Nome da disciplina
    - **ementa**: Descrição da ementa
    - **periodo**: Período sugerido para cursar a disciplina
    """
    return disciplina_service.cadastrar_disciplina(cadastro)

@router.get("/", response_model=List[DisciplinaResponse], summary="Listar disciplinas")
def listar_disciplinas():
    """
    Retorna uma lista com todas as disciplinas cadastradas.
    """
    return disciplina_service.listar_disciplinas()
