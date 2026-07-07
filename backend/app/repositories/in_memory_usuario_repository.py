"""
Implementação RAM do repositório de usuários.

Armazena dados em um dicionário interno — sem I/O de disco.
Ideal para testes e para subir a aplicação em modo efêmero.

Selecionada quando REPO_BACKEND=ram (ver app/repositories/factory.py).
"""

from typing import Dict, List, Optional, Tuple
from uuid import UUID

from app.models.usuario import Usuario
from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository


class InMemoryUsuarioRepository(AbstractUsuarioRepository):
    """Repositório de usuários com armazenamento em memória RAM."""

    def __init__(self) -> None:
        self._store: Dict[UUID, Usuario] = {}

    def add(self, usuario: Usuario) -> Usuario:
        self._store[usuario.id] = usuario
        return usuario

    def find_all(self) -> List[Usuario]:
        return list(self._store.values())

    def find_all_paginated(self, skip: int, limit: int) -> Tuple[List[Usuario], int]:
        todos = list(self._store.values())
        total = len(todos)
        pagina = todos[skip: skip + limit]
        return pagina, total

    def find_by_filters(
        self,
        nome: Optional[str],
        matricula: Optional[str],
        skip: int,
        limit: int,
    ) -> Tuple[List[Usuario], int]:
        resultado = list(self._store.values())

        if nome:
            termo = nome.strip().lower()
            resultado = [u for u in resultado if termo in u.nome.lower()]

        if matricula:
            termo_mat = matricula.strip()
            resultado = [
                u for u in resultado
                if getattr(u, "matricula", None) == termo_mat
            ]

        total = len(resultado)
        pagina = resultado[skip: skip + limit]
        return pagina, total

    def update(self, usuario: Usuario) -> Optional[Usuario]:
        if usuario.id not in self._store:
            return None
        self._store[usuario.id] = usuario
        return usuario

    def find_by_id(self, id: UUID) -> Optional[Usuario]:
        return self._store.get(id)

    def find_by_email(self, email: str) -> Optional[Usuario]:
        for u in self._store.values():
            if u.email == email:
                return u
        return None

    def find_by_login(self, login: str) -> Optional[Usuario]:
        for u in self._store.values():
            if u.login == login:
                return u
        return None

    def clear(self) -> None:
        self._store.clear()
