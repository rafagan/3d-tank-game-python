import time

from game.camera import Camera
from game.igame import IGame
from game.world import World
from util.decorator.singleton import singleton
from game.globals import Global
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from window.key_listener import KeyListener


@singleton
class Window:
    def __init__(self):
        self.window = None
        self.game = None

        self.start_loop_time = 0
        self.previous_loop_time = 0
        self.accumulated_rate = 0
        self.first_frames_to_skip = 60

        self.display_glut_bug = 0

    def run(self, game: IGame) -> None:
        self.game = game

        self.__init()
        try:
            self.__execute()
        except Exception as e:
            print(e)
            self.__terminate_gracefully()
            exit(0)

    def __init(self) -> None:
        # GLUT initialization
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

        # Window initialization
        glutInitWindowSize(Global().window_default_width, Global().window_default_height)
        self.window = glutCreateWindow(Global().window_title)
        try:
            glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
        except:
            ...

        # Window events
        glutIgnoreKeyRepeat(True)
        glutDisplayFunc(self.__display)
        glutIdleFunc(self.__game_loop)
        glutReshapeFunc(self.__reshape)
        glutKeyboardFunc(KeyListener().on_keyboard_pressed)
        glutSpecialFunc(KeyListener().on_keyboard_pressed)
        glutKeyboardUpFunc(KeyListener().on_keyboard_released)
        glutSpecialUpFunc(KeyListener().on_keyboard_released)

        # OpenGL initialization
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Light
        ambient_light = [0.4, 0.4, 0.4]
        diffuse_light = [0.7, 0.7, 0.7]
        specular_light = [0.9, 0.9, 0.9]
        light_position = [0.0, 0.0, 0.0]
        glEnable(GL_LIGHTING)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glEnable(GL_LIGHT0)

        # Material
        specular = [1.0, 1.0, 1.0]
        shininess = 51
        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMateriali(GL_FRONT, GL_SHININESS, shininess)

        self.game.init()

    def __execute(self) -> None:
        glutMainLoop()

    def __terminate_gracefully(self) -> None:
        self.game.terminate()
        try:
            glutLeaveMainLoop()
        except:
            ...
        glutDestroyWindow(glutGetWindow())

    def __display(self) -> None:
        self.display_glut_bug += 1
        if self.display_glut_bug % 2 == 0:
            return

        glClearColor(
            Global().clear_color.red(),
            Global().clear_color.green(),
            Global().clear_color.blue(),
            Global().clear_color.alpha()
        )
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        World().set_viewing_volume()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        Camera().update()
        self.game.draw()

        glutSwapBuffers()

    def __game_loop(self) -> None:
        self.start_loop_time = time.time()
        dt = self.start_loop_time - self.previous_loop_time
        self.previous_loop_time = self.start_loop_time

        if self.first_frames_to_skip > 0:
            self.first_frames_to_skip -= 1
            return

        self.accumulated_rate += dt
        Global().delta_time = dt

        if KeyListener().is_key_pressed(KeyListener().ESCAPE):
            self.__terminate_gracefully()

        self.game.update()
        KeyListener().update()
        if self.accumulated_rate > Global().goal_rate:
            self.accumulated_rate = 0
            glutPostRedisplay()

    def __reshape(self, w: int, h: int):
        Global().window_width = w
        Global().window_height = h
        glViewport(0, 0, w, h)
