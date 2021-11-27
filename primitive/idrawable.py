from abc import abstractmethod
from typing import Protocol

from util.gl_color import GlColor


class IDrawable(Protocol):
    @abstractmethod
    def get_color(self) -> GlColor:
        raise NotImplementedError

    @abstractmethod
    def set_color(self, color: GlColor) -> None:
        raise NotImplementedError

    def draw(self) -> None:
        raise NotImplementedError
