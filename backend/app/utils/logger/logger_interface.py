from typing import Protocol


class ILogger(Protocol):
    """
    Interface para o sistema de log.
    Implementa o padrão Adapter, permitindo trocar a biblioteca base (logging, loguru, etc)
    sem impactar o restante do sistema.
    """

    def info(self, message: str) -> None:
        """Registra uma mensagem informativa."""
        ...

    def error(self, message: str) -> None:
        """Registra uma mensagem de erro."""
        ...

    def warning(self, message: str) -> None:
        """Registra uma mensagem de aviso."""
        ...

    def debug(self, message: str) -> None:
        """Registra uma mensagem de depuração."""
        ...
