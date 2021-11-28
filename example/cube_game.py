import numpy as np

from game.camera import Camera
from game.globals import Global
from game.igame import IGame

from primitive.box import Box
from OpenGL.GL import *
from OpenGL.GLUT import *

from util.gl_color import GlColor
from window.key_listener import KeyListener


class CubeGame(IGame):
    def __init__(self):
        cube_colors = [
            # Front Face
            GlColor.red_color(),

            # Back face
            GlColor.blue_color(),

            # Top face
            GlColor.yellow_color(),

            # Bottom face
            GlColor.magenta_color(),

            # Right face
            GlColor.green_color(),

            # Left face
            GlColor.cyan_color()
        ]

        self.cube1 = Box()
        self.cube1.colors = cube_colors
        self.cube2 = Box()
        self.cube2.colors = cube_colors
        self.cube3 = Box()
        self.cube3.colors = cube_colors
        self.cube4 = Box()
        self.cube4.colors = cube_colors

        self.linear_speed = 1000
        self.angular_speed = 360
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

    def init(self) -> None:
        ...

    def terminate(self) -> None:
        ...

    def update(self) -> None:
        self.angle_x += self.angular_speed * 0.07 * Global().delta_time
        self.angle_y += self.angular_speed * 0.05 * Global().delta_time
        self.angle_z += self.angular_speed * 0.09 * Global().delta_time

        if KeyListener().is_key_pressed(GLUT_KEY_UP):
            Camera().move(self.linear_speed * Global().delta_time)
        if KeyListener().is_key_pressed(GLUT_KEY_DOWN):
            Camera().move(-self.linear_speed * Global().delta_time)
        if KeyListener().is_key_pressed(GLUT_KEY_LEFT):
            Camera().turn(-self.angular_speed * Global().delta_time)
        if KeyListener().is_key_pressed(GLUT_KEY_RIGHT):
            Camera().turn(self.angular_speed * Global().delta_time)

    def draw_cube(self, c: Box, v: np.array) -> None:
        glPushMatrix()
        glTranslatef(v[0], v[1], v[2])

        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)
        glRotatef(self.angle_z, 0, 0, 1)

        glScalef(50, 50, 50)

        c.draw()
        glPopMatrix()

    def draw(self) -> None:
        distance = 500
        self.draw_cube(self.cube1, np.array([0, 0, distance]))
        self.draw_cube(self.cube2, np.array([0, 0, -distance]))
        self.draw_cube(self.cube3, np.array([distance, 0, 0]))
        self.draw_cube(self.cube4, np.array([-distance, 0, 0]))
