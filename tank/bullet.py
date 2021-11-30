import numpy as np

from game.globals import Global
from primitive.idrawable import IDrawable
from primitive.sphere import Sphere
from util.gl_color import GlColor
from OpenGL.GL import *

from util.math.collision import ICollidable, ICollider, AABB


class Bullet(IDrawable, ICollidable):
    def __init__(self, start_position: np.array, direction: np.array, speed: float):
        self.position = start_position
        self.velocity = direction * speed
        self.size = np.array([0.4, 0.4, 0.4])
        self.collider = AABB()
        self.lifetime = 0
        self.max_lifetime = 5

        self.mesh = Sphere()
        self.mesh.color = GlColor.from_color(150, 75, 0, 255)

    def update(self) -> None:
        self.lifetime += Global().delta_time
        self.velocity += Global().gravity * Global().delta_time
        self.position += self.velocity * Global().delta_time
        self.collider.update(self.position, self.size[0], self.size[1], self.size[2])

    def draw(self) -> None:
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glScalef(self.size[0], self.size[1], self.size[2])
        self.mesh.draw()
        glPopMatrix()

        # self.collider.draw()

    def kill(self):
        self.lifetime = self.max_lifetime + 1

    def get_collider(self) -> ICollider:
        return self.collider

    def has_collision_with(self, other: ICollidable) -> bool:
        return self.collider.check_collision(other.get_collider())

    def on_collision_enter(self, other: ICollidable) -> None:
        from tank.tank import Tank
        from tank.wall import Wall
        from tank.ground import Ground
        from tank.scene_object import SceneObject, SceneObjectType

        if isinstance(other, Ground):
            print('Ground collision detected')

        if isinstance(other, Wall):
            print('Wall collision detected')

        if isinstance(other, Tank):
            print('Tank collision detected')

        if isinstance(other, SceneObject):
            if other.type == SceneObjectType.FRIEND:
                print('Friend collision detected')
            elif other.type == SceneObjectType.ENEMY:
                print('Enemy collision detected')
