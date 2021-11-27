from game.globals import Global
from game.igame import IGame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from window.key_listener import KeyListener


class BlinkGame(IGame):
    def init(self) -> None:
        ...

    def terminate(self) -> None:
        ...

    def update(self) -> None:
        print(f'Update: {Global().delta_time}')

    def draw(self) -> None:
        if KeyListener().is_key_pressed(b' '):
            glClearColor(1, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        print('Draw')
