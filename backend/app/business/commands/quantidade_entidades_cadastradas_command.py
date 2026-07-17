from app.business.commands.command import Command
from app.services.disciplina_service import DisciplinaService
from app.services.inscricao_monitoria_service import InscricaoMonitoriaService
from app.services.usuario_service import UsuarioService


class QuantidadeEntidadesCadastradasCommand(Command[int]):
    def __init__(
        self,
        usuario_service: UsuarioService,
        disciplina_service: DisciplinaService,
        inscricao_monitoria_service: InscricaoMonitoriaService,
    ) -> None:
        self._usuario_service = usuario_service
        self._disciplina_service = disciplina_service
        self._inscricao_monitoria_service = inscricao_monitoria_service

    def execute(self) -> int:
        return (
            self._usuario_service.contar_usuarios()
            + self._disciplina_service.contar_disciplinas()
            + self._inscricao_monitoria_service.contar_inscricoes()
        )
