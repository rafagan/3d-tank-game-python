from abc import abstractmethod
from typing import Protocol


class IDrawable(Protocol):
    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError
