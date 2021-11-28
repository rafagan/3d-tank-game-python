import numpy as np

from util.decorator.singleton import singleton
from OpenGL.GLU import *

from util.math import vector, to_radians


@singleton
class Camera:
    def __init__(self):
        self.look_at_magnitude = 100

        # Camera position
        self.eye = np.array([0.0, 0.0, 0.0])

        # To where camera is looking for
        self.target = np.array([0.0, 0.0, self.look_at_magnitude])

        # Camera top direction vector
        self.up = np.array([0.0, 1.0, 0.0])

    def update(self) -> None:
        gluLookAt(
            self.eye[0], self.eye[1], self.eye[2],
            self.target[0], self.target[1], self.target[2],
            self.up[0], self.up[1], self.up[2]
        )

    def direction(self) -> np.array:
        return vector.normalize(self.target - self.eye)

    def move(self, speed: float) -> None:
        velocity = vector.resize(self.direction(), speed)
        self.eye += np.array([velocity[0], 0.0, velocity[2]])
        self.target += np.array([velocity[0], 0.0, velocity[2]])

    def turn(self, speed: float):
        self.target = vector.resize(
            vector.rotate(
                self.direction(),
                to_radians(speed),
                self.up
            ),
            self.look_at_magnitude
        ) + self.eye
