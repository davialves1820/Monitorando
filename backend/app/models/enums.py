from enum import Enum

class TipoPerfil(str, Enum):
    DISCENTE = "DISCENTE"
    MONITOR = "MONITOR"
    DOCENTE = "DOCENTE"
    COORDENADOR = "COORDENADOR"
