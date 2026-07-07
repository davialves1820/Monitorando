"""
Implementação SQLite do repositório de inscrições de monitoria.
"""

import sqlite3
from typing import List, Optional
from uuid import UUID

from app.database import get_connection
from app.exceptions import DatabaseException
from app.models.inscricao_monitoria import InscricaoMonitoria
from app.repositories.abstract_inscricao_monitoria_repository import AbstractInscricaoMonitoriaRepository


def _row_para_inscricao(row: sqlite3.Row) -> InscricaoMonitoria:
    return InscricaoMonitoria(
        id=UUID(row["id"]),
        usuario_id=UUID(row["usuario_id"]),
        disciplina_id=UUID(row["disciplina_id"]),
        motivacao=row["motivacao"],
        status=row["status"],
    )


class SQLiteInscricaoMonitoriaRepository(AbstractInscricaoMonitoriaRepository):

    def clear(self) -> None:
        try:
            with get_connection() as conn:
                conn.execute("DELETE FROM inscricoes_monitoria")
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao limpar tabela de inscricoes de monitoria: {e}")

    def add(self, inscricao: InscricaoMonitoria) -> InscricaoMonitoria:
        sql = """
            INSERT INTO inscricoes_monitoria (
                id, usuario_id, disciplina_id, motivacao, status
            ) VALUES (
                :id, :usuario_id, :disciplina_id, :motivacao, :status
            )
        """
        try:
            with get_connection() as conn:
                conn.execute(sql, {
                    "id": str(inscricao.id),
                    "usuario_id": str(inscricao.usuario_id),
                    "disciplina_id": str(inscricao.disciplina_id),
                    "motivacao": inscricao.motivacao,
                    "status": inscricao.status,
                })
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao salvar inscricao de monitoria: {e}")
        return inscricao

    def find_all(self) -> List[InscricaoMonitoria]:
        try:
            with get_connection() as conn:
                rows = conn.execute("SELECT * FROM inscricoes_monitoria").fetchall()
            return [_row_para_inscricao(row) for row in rows]
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao listar inscricoes de monitoria: {e}")

    def find_by_id(self, id: UUID) -> Optional[InscricaoMonitoria]:
        try:
            with get_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM inscricoes_monitoria WHERE id = ?", (str(id),)
                ).fetchone()
            return _row_para_inscricao(row) if row else None
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao buscar inscricao de monitoria por ID: {e}")

    def update(self, inscricao: InscricaoMonitoria) -> Optional[InscricaoMonitoria]:
        sql = """
            UPDATE inscricoes_monitoria SET
                usuario_id = :usuario_id,
                disciplina_id = :disciplina_id,
                motivacao = :motivacao,
                status = :status
            WHERE id = :id
        """
        try:
            with get_connection() as conn:
                cursor = conn.execute(sql, {
                    "id": str(inscricao.id),
                    "usuario_id": str(inscricao.usuario_id),
                    "disciplina_id": str(inscricao.disciplina_id),
                    "motivacao": inscricao.motivacao,
                    "status": inscricao.status,
                })
                if cursor.rowcount == 0:
                    return None
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao atualizar inscricao de monitoria: {e}")
        return inscricao

    def delete(self, id: UUID) -> bool:
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "DELETE FROM inscricoes_monitoria WHERE id = ?", (str(id),)
                )
                return cursor.rowcount > 0
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao remover inscricao de monitoria: {e}")

    def count(self) -> int:
        try:
            with get_connection() as conn:
                return conn.execute("SELECT COUNT(*) FROM inscricoes_monitoria").fetchone()[0]
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao contar inscricoes de monitoria: {e}")
