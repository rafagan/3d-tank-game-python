from abc import abstractmethod
from typing import Protocol, runtime_checkable
from OpenGL.GL import *

import numpy as np

from game.globals import Global
from primitive.box import Box
from util.gl_color import GlColor


@runtime_checkable
class ICollider(Protocol):
    @abstractmethod
    def check_collision(self, other: 'ICollider') -> bool:
        raise NotImplementedError


@runtime_checkable
class ICollidable(Protocol):
    @abstractmethod
    def get_collider(self) -> ICollider:
        raise NotImplementedError

    @abstractmethod
    def has_collision_with(self, other: 'ICollidable') -> bool:
        raise NotImplementedError

    @abstractmethod
    def on_collision_enter(self, other: 'ICollidable') -> None:
        raise NotImplementedError


class AABB(ICollider):
    def __init__(self):
        self.position = np.array([0, 0, 0])
        self.width = 1
        self.height = 1
        self.depth = 1
        self.min = None
        self.max = None

        self.update_min_max()

    def update_min_max(self) -> None:
        hw = self.width / 2
        hh = self.height / 2
        hd = self.depth / 2
        self.min = np.array([-hw, -hh, -hd])
        self.max = np.array([hw, hh, hd])

    def update(self, position: np.array, width: int, height: int, depth: int) -> None:
        self.position = position
        self.width = width
        self.height = height
        self.depth = depth
        self.update_min_max()

    def draw(self):
        mesh = Box()
        GlColor.from_color(0, 255, 0, 255).gl_set()
        glPushMatrix()

        glTranslatef(
            self.position[0],
            self.position[1],
            self.position[2]
        )
        glScalef(self.width, self.height, self.depth)

        mesh.draw()
        glPopMatrix()
        Global().default_color.gl_set()

    def check_collision(self, other: ICollider) -> bool:
        if isinstance(other, AABB):
            mi = self.get_min()
            min_x = mi[0]
            min_y = mi[1]
            min_z = mi[2]

            ma = self.get_max()
            max_x = ma[0]
            max_y = ma[1]
            max_z = ma[2]

            omi = other.get_min()
            other_min_x = omi[0]
            other_min_y = omi[1]
            other_min_z = omi[2]

            oma = other.get_max()
            other_max_x = oma[0]
            other_max_y = oma[1]
            other_max_z = oma[2]

            return (
                (min_x <= other_max_x and max_x >= other_min_x) and
                (min_y <= other_max_y and max_y >= other_min_y) and
                (min_z <= other_max_z and max_z >= other_min_z)
            )

        raise Exception('Unsupported collider')

    def get_min(self) -> np.array:
        return self.position - self.min

    def get_max(self) -> np.array:
        return self.position + self.max
