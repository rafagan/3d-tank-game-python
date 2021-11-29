from enum import Enum

import numpy as np
from OpenGL.GL import *

from game.asset_manager import AssetManager
from game.world import World
from primitive.idrawable import IDrawable
from util.math.collision import ICollidable, ICollider, AABB


class SceneObjectType(Enum):
    FRIEND = 1
    ENEMY = 2


class SceneObject(IDrawable, ICollidable):
    def __init__(self, object_type: SceneObjectType, start_position: np.array, size: np.array):
        print(start_position)

        self.type = object_type
        self.mesh = (
            AssetManager().friend_mesh if object_type == SceneObjectType.FRIEND
            else AssetManager().enemy_mesh
        )
        self.collider = AABB()
        self.position = start_position
        self.size = size

        World().collidable_with_bullet.append(self)

    def update(self):
        self.collider.update(self.position, self.size[0], self.size[1], self.size[2])

    def draw(self) -> None:
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])

        if self.type == SceneObjectType.FRIEND:
            glScalef(0.1, 0.1, 0.1)
        else:
            glScalef(0.05, 0.05, 0.05)

        glScalef(self.size[0], self.size[1], self.size[2])
        self.mesh.draw()
        glPopMatrix()

    def get_collider(self) -> ICollider:
        return self.collider

    def has_collision_with(self, other: ICollidable) -> bool:
        return self.collider.check_collision(other.get_collider())

    def on_collision_enter(self, other: ICollidable) -> None:
        from tank.bullet import Bullet

        if isinstance(other, Bullet):
            other.kill()
