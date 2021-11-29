import re
import sys

import numpy as np
from OpenGL.GL import *

from game.globals import Global
from primitive.idrawable import IDrawable
from util.gl_color import GlColor
from util.math import vector


class TriMesh(IDrawable):
    def __init__(self, file_name):
        file_path = f'{Global().resources_path}/models/{file_name}'
        self.vertices = []
        self.colors = []
        self.normals = []

        with open(file_path) as file:
            for line in file:
                values = re.split('\\s+', line.rstrip())
                if len(values) < 9:
                    continue

                v1 = np.array([
                    float(values[0]),
                    float(values[1]),
                    float(values[2]),
                ])

                v2 = np.array([
                    float(values[3]),
                    float(values[4]),
                    float(values[5]),
                ])

                v3 = np.array([
                    float(values[6]),
                    float(values[7]),
                    float(values[8]),
                ])

                self.vertices.append(v1)
                self.vertices.append(v2)
                self.vertices.append(v3)
                self.normals.append(vector.normalize(np.cross(v1, v2)))

                if len(values) == 10:
                    self.colors.append(GlColor.from_hex(int(values[9], 0)))

        # self.center_mesh()
        self.normalize_mesh()

    def find_boundaries(self):
        min_boundary = np.array([float(sys.maxsize), float(sys.maxsize), float(sys.maxsize)])
        max_boundary = np.array([-float(sys.maxsize), -float(sys.maxsize), -float(sys.maxsize)])
        for vertex in self.vertices:
            for i in range(3):
                if min_boundary[i] < vertex[i]:
                    min_boundary[i] = vertex[i]

                if max_boundary[i] > vertex[i]:
                    max_boundary[i] = vertex[i]

        return min_boundary, max_boundary

    def center_mesh(self):
        min_boundary, max_boundary = self.find_boundaries()
        centroid = (max_boundary - min_boundary) / 2
        for i, _ in enumerate(self.vertices):
            self.vertices[i] -= centroid

    def normalize_mesh(self):
        min_boundary, max_boundary = self.find_boundaries()
        size = np.array([
            abs(min_boundary[0]) + abs(max_boundary[0]),
            abs(min_boundary[1]) + abs(max_boundary[1]),
            abs(min_boundary[2]) + abs(max_boundary[2])
        ])
        for i, _ in enumerate(self.vertices):
            for j in range(3):
                self.vertices[i][j] /= size[j]

    def draw(self) -> None:
        normal = None

        glPushMatrix()
        glScalef(10, 10, 10)
        glBegin(GL_TRIANGLES)
        for i, vertex in enumerate(self.vertices):
            if i % 3 == 0:
                if len(self.colors) > 0:
                    self.colors[i // 3].gl_set()

                normal = self.normals[i // 3]

            glNormal3f(normal[0], normal[1], normal[2])
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
        glPopMatrix()
