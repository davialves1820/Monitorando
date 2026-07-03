from fastapi import HTTPException
from typing import List
from uuid import UUID

from app.models.inscricao_monitoria import (
    InscricaoMonitoria,
    InscricaoMonitoriaAtualizacao,
    InscricaoMonitoriaCadastro,
    InscricaoMonitoriaResponse,
)
from app.repositories.disciplina_repository import disciplina_repository
from app.repositories.inscricao_monitoria_repository import inscricao_monitoria_repository
from app.repositories.usuario_repository import usuario_repository


class InscricaoMonitoriaService:
    def cadastrar_inscricao(self, cadastro: InscricaoMonitoriaCadastro) -> InscricaoMonitoria:
        self._validar_relacionamentos(cadastro.usuario_id, cadastro.disciplina_id)
        motivacao = self._validar_motivacao(cadastro.motivacao)

        inscricao = InscricaoMonitoria(
            usuario_id=cadastro.usuario_id,
            disciplina_id=cadastro.disciplina_id,
            motivacao=motivacao,
        )
        inscricao_monitoria_repository.add(inscricao)
        return inscricao

    def listar_inscricoes(self) -> List[InscricaoMonitoriaResponse]:
        return [
            self._to_response(inscricao)
            for inscricao in inscricao_monitoria_repository.find_all()
        ]

    def buscar_inscricao_por_id(self, id: UUID) -> InscricaoMonitoria:
        inscricao = inscricao_monitoria_repository.find_by_id(id)
        if inscricao is None:
            raise HTTPException(
                status_code=404,
                detail=f"Inscricao de monitoria com id '{id}' nao encontrada."
            )
        return inscricao

    def atualizar_inscricao(
        self,
        id: UUID,
        atualizacao: InscricaoMonitoriaAtualizacao,
    ) -> InscricaoMonitoria:
        self.buscar_inscricao_por_id(id)
        self._validar_relacionamentos(atualizacao.usuario_id, atualizacao.disciplina_id)
        motivacao = self._validar_motivacao(atualizacao.motivacao)
        status = self._validar_status(atualizacao.status)

        inscricao = InscricaoMonitoria(
            id=id,
            usuario_id=atualizacao.usuario_id,
            disciplina_id=atualizacao.disciplina_id,
            motivacao=motivacao,
            status=status,
        )
        inscricao_monitoria_repository.update(inscricao)
        return inscricao

    def remover_inscricao(self, id: UUID) -> None:
        removida = inscricao_monitoria_repository.delete(id)
        if not removida:
            raise HTTPException(
                status_code=404,
                detail=f"Inscricao de monitoria com id '{id}' nao encontrada."
            )

    def contar_inscricoes(self) -> int:
        return inscricao_monitoria_repository.count()

    def _validar_relacionamentos(self, usuario_id: UUID, disciplina_id: UUID) -> None:
        if usuario_repository.find_by_id(usuario_id) is None:
            raise HTTPException(
                status_code=404,
                detail=f"Usuario com id '{usuario_id}' nao encontrado."
            )
        disciplina_existe = any(
            disciplina.id == disciplina_id
            for disciplina in disciplina_repository.find_all()
        )
        if not disciplina_existe:
            raise HTTPException(
                status_code=404,
                detail=f"Disciplina com id '{disciplina_id}' nao encontrada."
            )

    def _validar_motivacao(self, motivacao: str) -> str:
        if not motivacao or not motivacao.strip():
            raise HTTPException(
                status_code=400,
                detail="Motivacao e obrigatoria."
            )
        return motivacao.strip()

    def _validar_status(self, status: str) -> str:
        status_normalizado = status.strip().upper() if status else ""
        status_validos = {"PENDENTE", "APROVADA", "REJEITADA"}
        if status_normalizado not in status_validos:
            raise HTTPException(
                status_code=400,
                detail="Status deve ser PENDENTE, APROVADA ou REJEITADA."
            )
        return status_normalizado

    def _to_response(self, inscricao: InscricaoMonitoria) -> InscricaoMonitoriaResponse:
        return InscricaoMonitoriaResponse(
            id=inscricao.id,
            usuario_id=inscricao.usuario_id,
            disciplina_id=inscricao.disciplina_id,
            motivacao=inscricao.motivacao,
            status=inscricao.status,
        )


inscricao_monitoria_service = InscricaoMonitoriaService()
