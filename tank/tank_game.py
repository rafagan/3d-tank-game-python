import numpy as np
from OpenGL.GLUT import *

from game.camera import Camera
from game.globals import Global
from game.igame import IGame
from tank.ground import Ground
from tank.tank import Tank
from util.math import vector
from window.key_listener import KeyListener


class TankGame(IGame):
    def __init__(self):
        self.ground = Ground()
        self.tank = Tank()

    def init(self) -> None:
        self.ground.position = np.array([0, 0, 0])
        self.tank.position = np.array([0.0, 1.0, -12])

        # Top view
        Camera().eye = np.array([0, 50, 0.1])
        Camera().target = np.array([0, 1, 0])

        # Back View
        # Camera().eye = np.array([0, 2, -34])
        # Camera().target = np.array([0, 0, 1])

    def terminate(self) -> None:
        ...

    def update(self) -> None:
        if KeyListener().is_key_pressed(GLUT_KEY_UP):
            self.tank.move_forward()
        if KeyListener().is_key_pressed(GLUT_KEY_DOWN):
            self.tank.move_backward()
        if KeyListener().is_key_pressed(GLUT_KEY_LEFT):
            self.tank.turn_left()
        if KeyListener().is_key_pressed(GLUT_KEY_RIGHT):
            self.tank.turn_right()

        self.ground.update()
        self.tank.update()

    def draw(self) -> None:
        self.ground.draw()
        self.tank.draw()

