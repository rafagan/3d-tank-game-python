import numpy as np

from util.decorator.singleton import singleton
from OpenGL.GLU import *


@singleton
class Camera:
    def __init__(self):
        # Camera position
        self.eye = np.array([0, 0, 0])

        # To where camera is looking for
        self.target = np.array([0, 0, 1])

        # Camera top direction vector
        self.up = np.array([0, 1, 0])

    def update(self):
        gluLookAt(
            self.eye[0], self.eye[1], self.eye[2],
            self.target[0], self.target[1], self.target[2],
            self.up[0], self.up[1], self.up[2]
        )
