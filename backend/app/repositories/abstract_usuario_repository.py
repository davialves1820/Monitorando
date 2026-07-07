"""
Interface abstrata do repositório de usuários.

Qualquer implementação concreta (RAM, SQLite, etc.) deve estender esta classe
e implementar todos os métodos aqui declarados.

Princípio aplicado: DIP — os services dependem desta abstração,
nunca de uma implementação concreta.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID

from app.models.usuario import Usuario


class AbstractUsuarioRepository(ABC):

    @abstractmethod
    def add(self, usuario: Usuario) -> Usuario:
        """Persiste um novo usuário. Retorna o objeto persistido."""
        ...

    @abstractmethod
    def find_all(self) -> List[Usuario]:
        """Retorna todos os usuários cadastrados."""
        ...

    @abstractmethod
    def find_all_paginated(self, skip: int, limit: int) -> Tuple[List[Usuario], int]:
        """
        Retorna a página solicitada e o total de registros.

        Args:
            skip:  número de registros a pular (offset).
            limit: tamanho da página.

        Returns:
            Tupla (lista de usuários da página, total de registros).
        """
        ...

    @abstractmethod
    def find_by_filters(
        self,
        nome: Optional[str],
        matricula: Optional[str],
        skip: int,
        limit: int,
    ) -> Tuple[List[Usuario], int]:
        """
        Filtra usuários por nome parcial (case-insensitive) e/ou matrícula exata.

        Returns:
            Tupla (lista filtrada e paginada, total de resultados filtrados).
        """
        ...

    @abstractmethod
    def update(self, usuario: Usuario) -> Optional[Usuario]:
        """
        Atualiza todos os campos de um usuário existente.

        Returns:
            O usuário atualizado, ou None se o ID não for encontrado.
        """
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> Optional[Usuario]:
        """Busca um usuário pelo ID (UUID). Retorna None se não encontrado."""
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca um usuário pelo e-mail. Retorna None se não encontrado."""
        ...

    @abstractmethod
    def find_by_login(self, login: str) -> Optional[Usuario]:
        """Busca um usuário pelo login. Retorna None se não encontrado."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove todos os registros (usado em testes para isolamento)."""
        ...
