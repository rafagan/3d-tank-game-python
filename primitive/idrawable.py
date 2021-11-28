from abc import abstractmethod
from typing import Protocol

from util.gl_color import GlColor


class IDrawable(Protocol):
    def draw(self) -> None:
        raise NotImplementedError
