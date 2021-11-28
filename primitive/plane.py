from logging import exception

import numpy as np
from OpenGL.GL import *

from game.globals import Global
from primitive.idrawable import IDrawable


class Plane(IDrawable):
    def __init__(self):
        self.color = Global().default_color.gl_set()

        self.vertices = [
            np.array([-1.0,  0, -1.0]),
            np.array([-1.0,  0,  1.0]),
            np.array([1.0,  0,  1.0]),
            np.array([1.0,  0, -1.0]),
        ]

    def set_color(self, color):
        self.color = color

    def draw(self) -> None:
        self.color.gl_set()

        glBegin(GL_QUADS)
        for i, vertex in enumerate(self.vertices):
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

        Global().default_color.gl_set()
