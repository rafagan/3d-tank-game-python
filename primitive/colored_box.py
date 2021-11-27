import numpy as np

from game.globals import Global
from primitive.idrawable import IDrawable
from util.gl_color import GlColor
from OpenGL.GL import *


class ColoredBox(IDrawable):
    def __init__(self):
        self.color = Global().default_color

        self.colors = [
            # Front Face
            GlColor.red_color(),

            # Back face
            GlColor.blue_color(),

            # Top face
            GlColor.yellow_color(),

            # Bottom face
            GlColor.magenta_color(),

            # Right face
            GlColor.red_color(),

            # Left face
            GlColor.cyan_color()
        ]

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

    def get_color(self) -> GlColor:
        return self.color

    def set_color(self, color: GlColor) -> None:
        self.color = color

    def draw(self) -> None:
        self.color.gl_set()

        glBegin(GL_QUADS)
        for i, vertex in enumerate(self.vertices):
            if i % 4 == 0:
                print(f'ok {i // 4}')
                self.colors[i // 4].gl_set()
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

        Global().default_color.gl_set()
