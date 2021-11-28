import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

from game.globals import Global
from primitive.idrawable import IDrawable


class Sphere(IDrawable):
    def __init__(self):
        self.resolution = 100
        self.color = Global().default_color

        self.vertices = [
            np.array([-0.5,  0, -0.5]),
            np.array([-0.5,  0,  0.5]),
            np.array([0.5,  0,  0.5]),
            np.array([0.5,  0, -0.5]),
        ]

    def set_color(self, color):
        self.color = color

    def draw(self) -> None:
        self.color.gl_set()
        glutSolidSphere(1.0, self.resolution, self.resolution)
        Global().default_color.gl_set()
