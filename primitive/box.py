from logging import exception

import numpy as np
from OpenGL.GL import *

from game.globals import Global
from primitive.idrawable import IDrawable
from util.math import vector


class Box(IDrawable):
    def __init__(self, texture_range=None):
        if texture_range is None:
            texture_range = np.array([0.0, 0.0, 1.0, 1.0])
        self.colors = []

        self.vertices = [
            # Front Face
            np.array([-0.5, -0.5,  0.5]),
            np.array([0.5, -0.5,  0.5]),
            np.array([0.5,  0.5,  0.5]),
            np.array([-0.5,  0.5,  0.5]),

            # Back Face
            np.array([-0.5, -0.5, -0.5]),
            np.array([-0.5,  0.5, -0.5]),
            np.array([0.5,  0.5, -0.5]),
            np.array([0.5, -0.5, -0.5]),

            # Top Face
            np.array([-0.5,  0.5, -0.5]),
            np.array([-0.5,  0.5,  0.5]),
            np.array([0.5,  0.5,  0.5]),
            np.array([0.5,  0.5, -0.5]),

            # Bottom Face
            np.array([-0.5, -0.5, -0.5]),
            np.array([0.5, -0.5, -0.5]),
            np.array([0.5, -0.5,  0.5]),
            np.array([-0.5, -0.5,  0.5]),

            # Right Face
            np.array([0.5, -0.5, -0.5]),
            np.array([0.5,  0.5, -0.5]),
            np.array([0.5,  0.5,  0.5]),
            np.array([0.5, -0.5,  0.5]),

            # Left Face
            np.array([-0.5, -0.5, -0.5]),
            np.array([-0.5, -0.5,  0.5]),
            np.array([-0.5,  0.5,  0.5]),
            np.array([-0.5,  0.5, -0.5]),
        ]

        self.normals = [
            vector.normalize(np.cross(self.vertices[0], self.vertices[1])),
            vector.normalize(np.cross(self.vertices[4], self.vertices[5])),
            vector.normalize(np.cross(self.vertices[8], self.vertices[9])),
            vector.normalize(np.cross(self.vertices[12], self.vertices[13])),
            vector.normalize(np.cross(self.vertices[16], self.vertices[17])),
            vector.normalize(np.cross(self.vertices[20], self.vertices[21])),
        ]

        self.texture_coords = [
            np.array([texture_range[0], texture_range[2]]),
            np.array([texture_range[1], texture_range[2]]),
            np.array([texture_range[1], texture_range[3]]),
            np.array([texture_range[0], texture_range[3]]),
        ]

    def set_face_colors(self, colors):
        if len(colors) != 6:
            raise exception('You must provide 6 colors, one for each face')
        self.colors = colors

    def draw(self) -> None:
        normal = None

        glBegin(GL_QUADS)
        for i, vertex in enumerate(self.vertices):
            if i % 4 == 0:
                j = i // 4
                if len(self.colors) == 6:
                    self.colors[j].gl_set()

                normal = self.normals[j]

            texture_coord = self.texture_coords[i % 4]
            glTexCoord2f(texture_coord[0], texture_coord[1])
            glNormal3f(normal[0], normal[1], normal[2])
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

        Global().default_color.gl_set()
