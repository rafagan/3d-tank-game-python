from game.globals import Global
from primitive.idrawable import IDrawable
from primitive.sphere import Sphere
from util.gl_color import GlColor
from OpenGL.GL import *


class Bullet(IDrawable):
    def __init__(self, start_position, direction, speed):
        self.position = start_position
        self.velocity = direction * speed

        self.mesh = Sphere()
        self.mesh.color = GlColor.from_color(150, 75, 0, 255)

    def update(self):
        self.velocity += Global().gravity * Global().delta_time
        self.position += self.velocity * Global().delta_time

    def draw(self) -> None:
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glScalef(0.5, 0.5, 0.5)
        self.mesh.draw()
        glPopMatrix()
