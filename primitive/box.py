from logging import exception

import numpy as np
from OpenGL.GL import *

from game.globals import Global
from primitive.idrawable import IDrawable


class Box(IDrawable):
    def __init__(self):
        self.colors = []

        self.vertices = [
            # Front Face
            np.array([-1.0, -1.0,  1.0]),
            np.array([1.0, -1.0,  1.0]),
            np.array([1.0,  1.0,  1.0]),
            np.array([-1.0,  1.0,  1.0]),

            # Back Face
            np.array([-1.0, -1.0, -1.0]),
            np.array([-1.0,  1.0, -1.0]),
            np.array([1.0,  1.0, -1.0]),
            np.array([1.0, -1.0, -1.0]),

            # Top Face
            np.array([-1.0,  1.0, -1.0]),
            np.array([-1.0,  1.0,  1.0]),
            np.array([1.0,  1.0,  1.0]),
            np.array([1.0,  1.0, -1.0]),

            # Bottom Face
            np.array([-1.0, -1.0, -1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([1.0, -1.0,  1.0]),
            np.array([-1.0, -1.0,  1.0]),

            # Right Face
            np.array([1.0, -1.0, -1.0]),
            np.array([1.0,  1.0, -1.0]),
            np.array([1.0,  1.0,  1.0]),
            np.array([1.0, -1.0,  1.0]),

            # Left Face
            np.array([-1.0, -1.0, -1.0]),
            np.array([-1.0, -1.0,  1.0]),
            np.array([-1.0,  1.0,  1.0]),
            np.array([-1.0,  1.0, -1.0]),
        ]

    def set_face_colors(self, colors):
        if len(colors) != 6:
            raise exception('You must provide 6 colors, one for each face')
        self.colors = colors

    def draw(self) -> None:
        glBegin(GL_QUADS)
        for i, vertex in enumerate(self.vertices):
            if len(self.colors) == 6 and i % 4 == 0:
                self.colors[i // 4].gl_set()

            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

        Global().default_color.gl_set()
