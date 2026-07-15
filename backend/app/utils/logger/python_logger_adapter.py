import logging
from app.utils.logger.logger_interface import ILogger


class PythonLoggerAdapter(ILogger):
    """
    Adapter que implementa a interface ILogger utilizando a biblioteca
    padrão 'logging' do Python.
    """

    def __init__(self, name: str = "Monitorando"):
        self._logger = logging.getLogger(name)
        
        # Configura o logger apenas se ele não tiver handlers configurados
        if not self._logger.hasHandlers():
            self._logger.setLevel(logging.INFO)
            
            # Cria um handler para saída no console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Formato do log: "[DATA-HORA] [NÍVEL] MENSAGEM"
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", 
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)
            
            self._logger.addHandler(console_handler)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)
