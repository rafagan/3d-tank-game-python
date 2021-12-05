import math

from OpenGL.GL import *
from OpenGL.GLU import *

from game.globals import Global
from util.decorator.singleton import singleton
from util.math.matrix import my_glu_perspective


@singleton
class World:
    def __init__(self):
        self.collidable_with_bullet = []

    @staticmethod
    def set_viewing_volume():
        # fovy: frustum open angle
        field_of_view = 45

        # How much near and far the frustum viewing volume should be
        near = 0.01
        far = 100.0

        my_glu_perspective(field_of_view, Global().aspect_ratio(), near, far)

