"""
Facade + Singleton (padrao GoF) que agrega operacoes da camada de negocio.

O padrao Singleton e preservado: apenas uma instancia existe em todo o processo.
A fachada registra Commands na primeira inicializacao via `initialize()`, chamada
no boot da aplicacao (main.py lifespan), mantendo o DIP.
"""

from __future__ import annotations

from typing import Any, cast

from app.business.commands import Command, QuantidadeEntidadesCadastradasCommand
from app.services.disciplina_service import DisciplinaService
from app.services.inscricao_monitoria_service import InscricaoMonitoriaService
from app.services.usuario_service import UsuarioService


class FacadeSingletonController:
    _instance: FacadeSingletonController | None = None
    QUANTIDADE_ENTIDADES_CADASTRADAS = "quantidade_entidades_cadastradas"

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
        """Registra os commands na unica instancia do Singleton."""
        if not self._initialized:
            self._commands: dict[str, Command[Any]] = {}
            self.register_command(
                self.QUANTIDADE_ENTIDADES_CADASTRADAS,
                QuantidadeEntidadesCadastradasCommand(
                    usuario_service=usuario_service,
                    disciplina_service=disciplina_service,
                    inscricao_monitoria_service=inscricao_monitoria_service,
                ),
            )
            self._initialized = True

    def register_command(self, nome: str, command: Command[Any]) -> None:
        self._commands[nome] = command

    def execute_command(self, nome: str) -> Any:
        try:
            return self._commands[nome].execute()
        except KeyError as exc:
            raise ValueError(f"Command '{nome}' nao registrado na fachada.") from exc

    def quantidade_entidades_cadastradas(self) -> int:
        return cast(
            int,
            self.execute_command(self.QUANTIDADE_ENTIDADES_CADASTRADAS),
        )


# Instancia unica. Os commands sao registrados no boot via initialize().
facade_singleton_controller = FacadeSingletonController()
