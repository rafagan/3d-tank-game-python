import numpy as np
from OpenGL.GL import *

from game.globals import Global
from primitive.idrawable import IDrawable
from util.math import vector


class Plane(IDrawable):
    def __init__(self, texture_range=None):
        if texture_range is None:
            texture_range = np.array([0.0, 0.0, 1.0, 1.0])
        self.color = Global().default_color

        self.vertices = [
            np.array([-0.5,  0, -0.5]),
            np.array([-0.5,  0,  0.5]),
            np.array([0.5,  0,  0.5]),
            np.array([0.5,  0, -0.5]),
        ]

        self.normal = vector.normalize(np.cross(self.vertices[0], self.vertices[1]))

        self.texture_coords = [
            np.array([texture_range[0], texture_range[2]]),
            np.array([texture_range[1], texture_range[2]]),
            np.array([texture_range[1], texture_range[3]]),
            np.array([texture_range[0], texture_range[3]]),
        ]

    def set_color(self, color):
        self.color = color

    def draw(self) -> None:
        self.color.gl_set()

        glBegin(GL_QUADS)
        for i, vertex in enumerate(self.vertices):
            glTexCoord2f(self.texture_coords[i][0], self.texture_coords[i][1])
            glNormal3f(self.normal[0], self.normal[1], self.normal[2])
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

        Global().default_color.gl_set()
