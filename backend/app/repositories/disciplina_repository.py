"""
Repositório de disciplinas com persistência em banco de dados SQLite.

Responsabilidades:
- Mapear objetos Disciplina para linhas SQL e vice-versa.
- Executar operações CRUD sobre a tabela `disciplinas`.
- Converter erros sqlite3.DatabaseError em DatabaseException.
"""

import sqlite3
from typing import List, Optional
from uuid import UUID

from app.database import get_connection
from app.exceptions import DatabaseException
from app.models.disciplina import Disciplina


def _row_para_disciplina(row: sqlite3.Row) -> Disciplina:
    """Converte uma linha da tabela `disciplinas` em objeto Disciplina."""
    return Disciplina(
        id=UUID(row["id"]),
        codigo=row["codigo"],
        nome=row["nome"],
        ementa=row["ementa"],
        periodo=row["periodo"],
    )


class DisciplinaRepository:
    """
    Repositório de disciplinas com persistência em SQLite.

    Cada método abre e fecha sua própria conexão, garantindo atomicidade
    e thread-safety para o contexto da aplicação.
    """

    def clear(self) -> None:
        """Remove todos os registros da tabela disciplinas (usado em testes)."""
        try:
            with get_connection() as conn:
                conn.execute("DELETE FROM disciplinas")
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao limpar tabela de disciplinas: {e}")

    def add(self, disciplina: Disciplina) -> Disciplina:
        """
        Persiste uma nova disciplina no banco de dados.

        Raises:
            DatabaseException: em caso de falha de escrita (ex.: UNIQUE constraint).
        """
        sql = """
            INSERT INTO disciplinas (id, codigo, nome, ementa, periodo)
            VALUES (:id, :codigo, :nome, :ementa, :periodo)
        """
        try:
            with get_connection() as conn:
                conn.execute(sql, {
                    "id":      str(disciplina.id),
                    "codigo":  disciplina.codigo,
                    "nome":    disciplina.nome,
                    "ementa":  disciplina.ementa,
                    "periodo": disciplina.periodo,
                })
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao salvar disciplina: {e}")
        return disciplina

    def find_all(self) -> List[Disciplina]:
        """Retorna todas as disciplinas cadastradas."""
        try:
            with get_connection() as conn:
                rows = conn.execute("SELECT * FROM disciplinas").fetchall()
            return [_row_para_disciplina(r) for r in rows]
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao listar disciplinas: {e}")

    def find_by_codigo(self, codigo: str) -> Optional[Disciplina]:
        """
        Busca uma disciplina pelo código (exato, case-sensitive).
        Retorna None se não encontrada.
        """
        try:
            with get_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM disciplinas WHERE codigo = ?", (codigo,)
                ).fetchone()
            return _row_para_disciplina(row) if row else None
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao buscar disciplina por código: {e}")


# Instância global — mesma interface de antes, agora com SQLite por baixo
disciplina_repository = DisciplinaRepository()
