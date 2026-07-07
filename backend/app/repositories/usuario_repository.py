"""
Implementação SQLite do repositório de usuários.

Responsabilidades:
- Mapear objetos de domínio (Discente, Docente, Monitor) para linhas SQL.
- Executar operações CRUD sobre a tabela `usuarios`.
- Converter erros sqlite3.DatabaseError em DatabaseException.

Selecionada quando REPO_BACKEND=sqlite (padrão) — ver app/repositories/factory.py.
"""

import json
import sqlite3
from typing import List, Optional, Tuple
from uuid import UUID

from app.database import get_connection
from app.exceptions import DatabaseException
from app.models.enums import TipoPerfil
from app.models.usuario import Discente, Docente, Monitor, Usuario
from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
_TIPO_DISCENTE = "DISCENTE"
_TIPO_DOCENTE  = "DOCENTE"
_TIPO_MONITOR  = "MONITOR"


def _serializar_lista(lista: List[str]) -> str:
    """Converte uma lista de strings para JSON (armazenamento em TEXT)."""
    return json.dumps(lista, ensure_ascii=False)


def _deserializar_lista(texto: Optional[str]) -> List[str]:
    """Converte JSON armazenado em TEXT de volta para lista de strings."""
    if not texto:
        return []
    return json.loads(texto)


def _row_para_usuario(row: sqlite3.Row) -> Usuario:
    """
    Converte uma linha do banco de dados no objeto de domínio correto
    (Discente, Docente ou Monitor), baseado na coluna `tipo`.
    """
    tipo = row["tipo"]

    if tipo == _TIPO_MONITOR:
        return Monitor(
            id=UUID(row["id"]),
            nome=row["nome"],
            login=row["login"],
            email=row["email"],
            senha=row["senha"],
            perfil=TipoPerfil(row["perfil"]),
            ativo=bool(row["ativo"]),
            matricula=row["matricula"] or "",
            curso=row["curso"] or "",
            periodo=row["periodo"],
            disciplinasInteresse=_deserializar_lista(row["disciplinas_interesse"]),
            cargaHoraria=row["carga_horaria"] or 0,
            disponivel=bool(row["disponivel"]) if row["disponivel"] is not None else True,
            disciplinaVinculada=row["disciplina_vinculada"] or "",
        )

    if tipo == _TIPO_DISCENTE:
        return Discente(
            id=UUID(row["id"]),
            nome=row["nome"],
            login=row["login"],
            email=row["email"],
            senha=row["senha"],
            perfil=TipoPerfil(row["perfil"]),
            ativo=bool(row["ativo"]),
            matricula=row["matricula"] or "",
            curso=row["curso"] or "",
            periodo=row["periodo"],
            disciplinasInteresse=_deserializar_lista(row["disciplinas_interesse"]),
        )

    # Docente (tipo == _TIPO_DOCENTE ou qualquer outro)
    return Docente(
        id=UUID(row["id"]),
        nome=row["nome"],
        login=row["login"],
        email=row["email"],
        senha=row["senha"],
        perfil=TipoPerfil(row["perfil"]),
        ativo=bool(row["ativo"]),
        siape=row["siape"] or "",
        departamento=row["departamento"] or "",
        isCoordenador=bool(row["is_coordenador"]) if row["is_coordenador"] is not None else False,
        disciplinas=_deserializar_lista(row["disciplinas_docente"]),
    )


def _usuario_para_params(usuario: Usuario) -> dict:
    """
    Converte um objeto de domínio em um dicionário de parâmetros para INSERT/UPDATE.
    Usa discriminador `tipo` para representar a herança no modelo relacional.
    """
    params: dict = {
        "id":          str(usuario.id),
        "nome":        usuario.nome,
        "login":       usuario.login,
        "email":       usuario.email,
        "senha":       usuario.senha,
        "perfil":      usuario.perfil.value,
        "ativo":       int(usuario.ativo),
        # Atributos específicos — preenchidos conforme o tipo
        "matricula":               None,
        "curso":                   None,
        "periodo":                 None,
        "disciplinas_interesse":   None,
        "siape":                   None,
        "departamento":            None,
        "is_coordenador":          None,
        "disciplinas_docente":     None,
        "carga_horaria":           None,
        "disponivel":              None,
        "disciplina_vinculada":    None,
    }

    if isinstance(usuario, Monitor):
        params["tipo"]                   = _TIPO_MONITOR
        params["matricula"]              = usuario.matricula
        params["curso"]                  = usuario.curso
        params["periodo"]                = usuario.periodo
        params["disciplinas_interesse"]  = _serializar_lista(usuario.disciplinasInteresse)
        params["carga_horaria"]          = usuario.cargaHoraria
        params["disponivel"]             = int(usuario.disponivel)
        params["disciplina_vinculada"]   = usuario.disciplinaVinculada

    elif isinstance(usuario, Discente):
        params["tipo"]                   = _TIPO_DISCENTE
        params["matricula"]              = usuario.matricula
        params["curso"]                  = usuario.curso
        params["periodo"]                = usuario.periodo
        params["disciplinas_interesse"]  = _serializar_lista(usuario.disciplinasInteresse)

    else:  # Docente
        params["tipo"]                   = _TIPO_DOCENTE
        params["siape"]                  = getattr(usuario, "siape", "")
        params["departamento"]           = getattr(usuario, "departamento", "")
        params["is_coordenador"]         = int(getattr(usuario, "isCoordenador", False))
        params["disciplinas_docente"]    = _serializar_lista(getattr(usuario, "disciplinas", []))

    return params


class SQLiteUsuarioRepository(AbstractUsuarioRepository):
    """
    Repositório de usuários com persistência em SQLite.

    Todos os métodos abrem e fecham sua própria conexão (padrão conexão curta),
    garantindo que cada operação seja atômica e thread-safe para o contexto
    da aplicação.
    """

    def clear(self) -> None:
        """Remove todos os registros da tabela usuarios (usado em testes)."""
        try:
            with get_connection() as conn:
                conn.execute("DELETE FROM usuarios")
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao limpar tabela de usuários: {e}")

    def add(self, usuario: Usuario) -> Usuario:
        """
        Persiste um novo usuário no banco de dados.

        Raises:
            DatabaseException: em caso de falha de escrita (ex.: UNIQUE constraint).
        """
        params = _usuario_para_params(usuario)
        sql = """
            INSERT INTO usuarios (
                id, nome, login, email, senha, perfil, ativo, tipo,
                matricula, curso, periodo, disciplinas_interesse,
                siape, departamento, is_coordenador, disciplinas_docente,
                carga_horaria, disponivel, disciplina_vinculada
            ) VALUES (
                :id, :nome, :login, :email, :senha, :perfil, :ativo, :tipo,
                :matricula, :curso, :periodo, :disciplinas_interesse,
                :siape, :departamento, :is_coordenador, :disciplinas_docente,
                :carga_horaria, :disponivel, :disciplina_vinculada
            )
        """
        try:
            with get_connection() as conn:
                conn.execute(sql, params)
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao salvar usuário: {e}")
        return usuario

    def find_all(self) -> List[Usuario]:
        """Retorna todos os usuários cadastrados."""
        try:
            with get_connection() as conn:
                rows = conn.execute("SELECT * FROM usuarios").fetchall()
            return [_row_para_usuario(r) for r in rows]
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao listar usuários: {e}")

    def find_all_paginated(self, skip: int, limit: int) -> Tuple[List[Usuario], int]:
        """
        Retorna a página solicitada e o total de registros.

        Args:
            skip:  número de registros a pular (offset).
            limit: tamanho da página.
        """
        try:
            with get_connection() as conn:
                total = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
                rows  = conn.execute(
                    "SELECT * FROM usuarios LIMIT :limit OFFSET :skip",
                    {"limit": limit, "skip": skip}
                ).fetchall()
            return [_row_para_usuario(r) for r in rows], total
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao listar usuários paginados: {e}")

    def find_by_filters(
        self,
        nome: Optional[str],
        matricula: Optional[str],
        skip: int,
        limit: int,
    ) -> Tuple[List[Usuario], int]:
        """
        Filtra usuários por nome parcial (case-insensitive) e/ou matrícula exata.
        Retorna a fatia paginada e o total de resultados filtrados.
        """
        conditions: List[str] = []
        params: dict = {}

        if nome:
            conditions.append("LOWER(nome) LIKE :nome_like")
            params["nome_like"] = f"%{nome.strip().lower()}%"

        if matricula:
            conditions.append("matricula = :matricula")
            params["matricula"] = matricula.strip()

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        try:
            with get_connection() as conn:
                total = conn.execute(
                    f"SELECT COUNT(*) FROM usuarios {where}", params
                ).fetchone()[0]

                params["limit"] = limit
                params["skip"]  = skip
                rows = conn.execute(
                    f"SELECT * FROM usuarios {where} LIMIT :limit OFFSET :skip",
                    params
                ).fetchall()

            return [_row_para_usuario(r) for r in rows], total
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao filtrar usuários: {e}")

    def update(self, usuario: Usuario) -> Optional[Usuario]:
        """
        Atualiza todos os campos de um usuário existente.

        Returns:
            O usuário atualizado, ou None se o ID não for encontrado.
        """
        params = _usuario_para_params(usuario)
        sql = """
            UPDATE usuarios SET
                nome = :nome, login = :login, email = :email, senha = :senha,
                perfil = :perfil, ativo = :ativo, tipo = :tipo,
                matricula = :matricula, curso = :curso, periodo = :periodo,
                disciplinas_interesse = :disciplinas_interesse,
                siape = :siape, departamento = :departamento,
                is_coordenador = :is_coordenador,
                disciplinas_docente = :disciplinas_docente,
                carga_horaria = :carga_horaria, disponivel = :disponivel,
                disciplina_vinculada = :disciplina_vinculada
            WHERE id = :id
        """
        try:
            with get_connection() as conn:
                cursor = conn.execute(sql, params)
                if cursor.rowcount == 0:
                    return None
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao atualizar usuário: {e}")
        return usuario

    def find_by_id(self, id: UUID) -> Optional[Usuario]:
        """Busca um usuário pelo ID (UUID). Retorna None se não encontrado."""
        try:
            with get_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM usuarios WHERE id = ?", (str(id),)
                ).fetchone()
            return _row_para_usuario(row) if row else None
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao buscar usuário por ID: {e}")

    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca um usuário pelo e-mail. Retorna None se não encontrado."""
        try:
            with get_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM usuarios WHERE email = ?", (email,)
                ).fetchone()
            return _row_para_usuario(row) if row else None
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao buscar usuário por e-mail: {e}")

    def find_by_login(self, login: str) -> Optional[Usuario]:
        """Busca um usuário pelo login. Retorna None se não encontrado."""
        try:
            with get_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM usuarios WHERE login = ?", (login,)
                ).fetchone()
            return _row_para_usuario(row) if row else None
        except sqlite3.DatabaseError as e:
            raise DatabaseException(f"Erro ao buscar usuário por login: {e}")
