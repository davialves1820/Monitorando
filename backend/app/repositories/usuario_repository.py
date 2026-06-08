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
