from fastapi import APIRouter
from pydantic import BaseModel

from app.controllers.facade_singleton_controller import facade_singleton_controller


class QuantidadeEntidadesResponse(BaseModel):
    quantidade: int


router = APIRouter(prefix="/facade", tags=["Facade Singleton"])


@router.get("/quantidade-entidades", response_model=QuantidadeEntidadesResponse)
def quantidade_entidades_cadastradas():
    return QuantidadeEntidadesResponse(
        quantidade=facade_singleton_controller.quantidade_entidades_cadastradas()
    )
