from abc import abstractmethod
from typing import Protocol, runtime_checkable

import numpy as np


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

    def check_collision(self, other: ICollider) -> bool:
        if isinstance(other, AABB):
            mi = self.get_min()
            ma = self.get_max()
            omi = other.get_min()
            oma = other.get_max()

            for i in range(3):
                if ma[i] < omi[i]:
                    return False
                if mi[i] > oma[i]:
                    return False

            return True

        raise Exception('Unsupported collider')

    def get_min(self) -> np.array:
        return self.position - self.min

    def get_max(self) -> np.array:
        return self.position + self.max
