"""
Facade + Singleton (padrão GoF) que agrega os três services do sistema.

O padrão Singleton é preservado: apenas uma instância existe em todo o processo.
A injeção dos services acontece na primeira inicialização via `initialize()`,
chamada no boot da aplicação (main.py lifespan), mantendo o DIP.
"""

from __future__ import annotations

from app.services.disciplina_service import DisciplinaService
from app.services.inscricao_monitoria_service import InscricaoMonitoriaService
from app.services.usuario_service import UsuarioService


class FacadeSingletonController:
    _instance: FacadeSingletonController | None = None

    def __new__(cls) -> FacadeSingletonController:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize(
        self,
        usuario_service: UsuarioService,
        disciplina_service: DisciplinaService,
        inscricao_monitoria_service: InscricaoMonitoriaService,
    ) -> None:
        """Injeta os services na única instância do Singleton."""
        if not self._initialized:
            self.usuario_service             = usuario_service
            self.disciplina_service          = disciplina_service
            self.inscricao_monitoria_service = inscricao_monitoria_service
            self._initialized = True

    def quantidade_entidades_cadastradas(self) -> int:
        """
        Conta o total de entidades via services — funciona tanto com o
        backend RAM quanto com o SQLite, sem acesso direto ao banco.
        """
        usuarios   = len(self.usuario_service._repo.find_all())
        disciplinas = len(self.disciplina_service._repo.find_all())
        inscricoes  = len(self.inscricao_monitoria_service._inscricao_repo.find_all())
        return usuarios + disciplinas + inscricoes


# Instância única — os services são injetados no boot via initialize()
facade_singleton_controller = FacadeSingletonController()
