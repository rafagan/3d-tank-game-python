import numpy as np

from game.camera import Camera
from game.globals import Global
from primitive.box import Box
from primitive.idrawable import IDrawable
from util.gl_color import GlColor
from OpenGL.GL import *

from util.math import vector, to_radians


class Tank(IDrawable):
    def __init__(self):
        self.position = np.array([0.0, -200.0, 800.0])
        # self.position = np.array([0.0, 0, 800.0])
        self.angle = 0
        self.linear_speed = 1.0
        self.angular_speed = 30.0

        self.box = Box()

    def get_color(self) -> GlColor:
        pass

    def set_color(self, color: GlColor) -> None:
        pass

    def __move(self, sense):
        linear_velocity_xz = vector.from_size_and_angle(
            sense * self.linear_speed, to_radians(self.angle + 90)
        )
        offset_xz = linear_velocity_xz * Global().delta_time
        self.position += np.array([offset_xz[0], 0, offset_xz[1]])

        offset = self.linear_speed * Global().delta_time * sense
        Camera().move(offset)

    def __turn(self, clock_sense):
        angular_velocity = self.angular_speed * clock_sense
        delta = angular_velocity * Global().delta_time
        self.angle += delta
        Camera().turn(delta)

    def move_forward(self):
        self.__move(1)

    def move_backward(self):
        self.__move(-1)

    def turn_left(self):
        self.__turn(1)

    def turn_right(self):
        self.__turn(-1)

    def update(self):
        ...

    def draw(self) -> None:
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.angle, 0, 1, 0)
        glScalef(320, 50, 200)

        self.box.draw()
        glPopMatrix()
