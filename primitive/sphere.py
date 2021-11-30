import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from game.globals import Global
from primitive.idrawable import IDrawable


class Sphere(IDrawable):
    def __init__(self):
        self.resolution = 100
        self.color = Global().default_color

    def set_color(self, color):
        self.color = color

    def draw(self) -> None:
        self.color.gl_set()

        sphere = gluNewQuadric()
        gluQuadricDrawStyle(sphere, GLU_FILL)
        gluQuadricNormals(sphere, GLU_SMOOTH)
        gluQuadricOrientation(sphere, GLU_OUTSIDE)
        gluSphere(sphere, 1.0, self.resolution, self.resolution)

        Global().default_color.gl_set()
