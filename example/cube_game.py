from game.globals import Global
from game.igame import IGame

from primitive.box import Box
from OpenGL.GL import *

from primitive.colored_box import ColoredBox


class CubeGame(IGame):
    def __init__(self):
        self.cube = ColoredBox()

        self.angular_velocity = 1000
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

    def init(self) -> None:
        ...

    def terminate(self) -> None:
        ...

    def update(self) -> None:
        self.angle_x += self.angular_velocity * 0.07 * Global().delta_time
        self.angle_y += self.angular_velocity * 0.05 * Global().delta_time
        self.angle_z += self.angular_velocity * 0.09 * Global().delta_time

    def draw(self) -> None:
        glPushMatrix()
        glTranslatef(0.0, 0.0, -50)

        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)
        glRotatef(self.angle_z, 0, 0, 1)

        glScalef(5, 5, 5)

        self.cube.draw()
        glPopMatrix()
