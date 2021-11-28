import math

import numpy as np
from OpenGL.GL import *

from game.globals import Global
from primitive.idrawable import IDrawable
from util.math import to_radians


class Cylinder(IDrawable):
    def __init__(self):
        self.resolution = 100
        self.color = Global().default_color

    def set_color(self, color):
        self.color = color

    def draw(self) -> None:
        self.color.gl_set()

        glDisable(GL_CULL_FACE)
        glBegin(GL_QUAD_STRIP)
        for i in range(361):
            c = math.cos(to_radians(i))
            s = math.sin(to_radians(i))
            glVertex3f(c, 0.5, s)
            glVertex3f(c, -0.5, s)
        glEnd()
        glEnable(GL_CULL_FACE)

        Global().default_color.gl_set()
