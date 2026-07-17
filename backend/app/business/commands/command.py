from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ResultadoCommand = TypeVar("ResultadoCommand")


class Command(ABC, Generic[ResultadoCommand]):
    @abstractmethod
    def execute(self) -> ResultadoCommand:
        ...
