import numpy as np
from OpenGL.GLUT import *

from game.camera import Camera
from game.igame import IGame
from game.world import World
from tank.wall import Wall
from tank.ground import Ground
from tank.tank import Tank
from window.key_listener import KeyListener


class TankGame(IGame):
    def __init__(self):
        self.ground = Ground()
        self.wall = Wall()
        self.tank = Tank()

    def init(self) -> None:
        self.tank.position = np.array([0.0, 1.0, -self.ground.grid_depth / 2])

        # Top view
        Camera().eye = np.array([0.0, 50.0, 0.1])
        Camera().target = np.array([0.0, 0.0, 0.0])

        # Back View
        # Camera().eye = np.array([0.0, 5.0, -35.0])
        # Camera().target = np.array([0.0, 10.0, 0.0])

        # Left View
        # Camera().eye = np.array([-45.0, 5.0, -10.0])
        # Camera().target = np.array([0.0, 10.0, 0.0])

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
        self.wall.update()
        self.tank.update()

    def draw(self) -> None:
        self.ground.draw()
        self.wall.draw()
        self.tank.draw()

