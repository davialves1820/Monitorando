from fastapi import APIRouter, status
from typing import List
from uuid import UUID

from app.models.inscricao_monitoria import (
    InscricaoMonitoriaAtualizacao,
    InscricaoMonitoriaCadastro,
    InscricaoMonitoriaResponse,
)
from app.services.inscricao_monitoria_service import inscricao_monitoria_service

router = APIRouter(prefix="/inscricoes-monitoria", tags=["Inscricoes de Monitoria"])


@router.post("/", response_model=InscricaoMonitoriaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_inscricao(cadastro: InscricaoMonitoriaCadastro):
    return inscricao_monitoria_service.cadastrar_inscricao(cadastro)


@router.get("/", response_model=List[InscricaoMonitoriaResponse])
def listar_inscricoes():
    return inscricao_monitoria_service.listar_inscricoes()


@router.get("/{id}", response_model=InscricaoMonitoriaResponse)
def detalhar_inscricao(id: UUID):
    return inscricao_monitoria_service.buscar_inscricao_por_id(id)


@router.put("/{id}", response_model=InscricaoMonitoriaResponse)
def atualizar_inscricao(id: UUID, atualizacao: InscricaoMonitoriaAtualizacao):
    return inscricao_monitoria_service.atualizar_inscricao(id, atualizacao)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_inscricao(id: UUID):
    inscricao_monitoria_service.remover_inscricao(id)
