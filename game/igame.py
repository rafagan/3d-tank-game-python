from abc import abstractmethod
from typing import Protocol


class IGame(Protocol):
    @abstractmethod
    def init(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def terminate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError
