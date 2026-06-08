from typing import List, Optional
from uuid import UUID
from app.models.usuario import Usuario

class UsuarioRepository:
    def __init__(self):
        self._usuarios: List[Usuario] = []

    def add(self, usuario: Usuario) -> Usuario:
        self._usuarios.append(usuario)
        return usuario

    def find_all(self) -> List[Usuario]:
        return self._usuarios

    def find_all_paginated(self, skip: int, limit: int) -> tuple[List[Usuario], int]:
        """Retorna a página solicitada e o total de registros."""
        total = len(self._usuarios)
        pagina = self._usuarios[skip: skip + limit]
        return pagina, total

    def find_by_filters(
        self,
        nome: Optional[str],
        matricula: Optional[str],
        skip: int,
        limit: int,
    ) -> tuple[List[Usuario], int]:
        """
        Filtra usuários por nome parcial (case-insensitive) e/ou matrícula exata.
        Retorna a fatia paginada e o total de resultados filtrados.
        """
        resultado = self._usuarios

        if nome:
            nome_lower = nome.strip().lower()
            resultado = [u for u in resultado if nome_lower in u.nome.lower()]

        if matricula:
            matricula_strip = matricula.strip()
            # Apenas Discente tem o atributo 'matricula'
            resultado = [
                u for u in resultado
                if hasattr(u, "matricula") and u.matricula == matricula_strip
            ]

        total = len(resultado)
        pagina = resultado[skip: skip + limit]
        return pagina, total


    def update(self, usuario: Usuario) -> Optional[Usuario]:
        for i, u in enumerate(self._usuarios):
            if u.id == usuario.id:
                self._usuarios[i] = usuario
                return usuario
        return None

    def find_by_id(self, id: UUID) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.id == id:
                return usuario
        return None

    def find_by_email(self, email: str) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.email == email:
                return usuario
        return None

# Instância global para simular o banco de dados em memória
usuario_repository = UsuarioRepository()
