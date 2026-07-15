from app.utils.logger.logger_interface import ILogger
from app.utils.logger.python_logger_adapter import PythonLoggerAdapter

_logger_instance: ILogger | None = None


def get_logger() -> ILogger:
    """
    Factory para obter a instância do logger configurada.
    Garante que a mesma instância do Adapter seja utilizada.
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = PythonLoggerAdapter()
    return _logger_instance
