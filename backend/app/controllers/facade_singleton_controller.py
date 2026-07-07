from app.database import get_connection
from app.services.disciplina_service import disciplina_service
from app.services.inscricao_monitoria_service import inscricao_monitoria_service
from app.services.usuario_service import usuario_service


class FacadeSingletonController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FacadeSingletonController, cls).__new__(cls)
            cls._instance.usuario_service = usuario_service
            cls._instance.disciplina_service = disciplina_service
            cls._instance.inscricao_monitoria_service = inscricao_monitoria_service
        return cls._instance

    def quantidade_entidades_cadastradas(self) -> int:
        with get_connection() as conn:
            usuarios = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
            disciplinas = conn.execute("SELECT COUNT(*) FROM disciplinas").fetchone()[0]
            inscricoes = conn.execute(
                "SELECT COUNT(*) FROM inscricoes_monitoria"
            ).fetchone()[0]
        return usuarios + disciplinas + inscricoes


facade_singleton_controller = FacadeSingletonController()
