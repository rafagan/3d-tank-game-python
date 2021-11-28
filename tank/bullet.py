import numpy as np

from game.globals import Global
from primitive.idrawable import IDrawable
from primitive.sphere import Sphere
from tank.ground import Ground
from tank.wall import Wall
from util.gl_color import GlColor
from OpenGL.GL import *

from util.math.collision import ICollidable, ICollider, AABB


class Bullet(IDrawable, ICollidable):
    def __init__(self, start_position: np.array, direction: np.array, speed: float):
        self.position = start_position
        self.velocity = direction * speed
        self.size = np.array([0.5, 0.5, 0.5])
        self.collider = AABB()

        self.mesh = Sphere()
        self.mesh.color = GlColor.from_color(150, 75, 0, 255)

    def update(self) -> None:
        self.velocity += Global().gravity * Global().delta_time
        self.position += self.velocity * Global().delta_time
        self.collider.update(self.position, self.size[0], self.size[1], self.size[2])

    def draw(self) -> None:
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glScalef(self.size[0], self.size[1], self.size[2])
        self.mesh.draw()
        glPopMatrix()

    def get_collider(self) -> ICollider:
        return self.collider

    def has_collision_with(self, other: ICollidable) -> bool:
        return self.collider.check_collision(other.get_collider())

    def on_collision_enter(self, other: ICollidable) -> None:
        if isinstance(other, Ground):
            print('Collidiu com Ground')

        if isinstance(other, Wall):
            print('Collidiu com Wall')
