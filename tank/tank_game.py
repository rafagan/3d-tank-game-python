import numpy as np
from OpenGL.GLUT import *

from game.camera import Camera
from game.globals import Global
from game.igame import IGame
from game.world import World
from tank.scene_object import SceneObject, SceneObjectType
from tank.wall import Wall
from tank.ground import Ground
from tank.tank import Tank
from util.math import vector, to_radians
from util.math.collision import AABB
from window.key_listener import KeyListener


class TankGame(IGame):
    def __init__(self):
        self.ground = Ground()
        self.wall = Wall()
        self.tank = Tank()

        self.camera_angle = 180

        self.aabb = AABB()
        self.aabb.update(np.array([0, 0, 0]), 1, 1, 1)

        self.scene_objects = []
        for i in range(1):
            self.scene_objects.append(SceneObject(
                SceneObjectType.FRIEND,
                np.array([-10, 2.5, 0]),
                np.array([5, 5, 5])
            ))

    def init(self) -> None:
        self.tank.position = np.array([-self.ground.grid_width / 2, 1.0, 0.0])

        # Top view
        # Camera().eye = np.array([0.0, 50.0, 0.1])
        # Camera().target = np.array([0.0, 0.0, 0.0])

        # Back View
        # Camera().eye = np.array([0.0, 5.0, -35.0])
        # Camera().target = np.array([0.0, 10.0, 0.0])

        # Left View
        # Camera().eye = np.array([-45.0, 5.0, -10.0])
        # Camera().target = np.array([0.0, 10.0, 0.0])

    def terminate(self) -> None:
        ...

    def rotate_camera_around(self):
        self.camera_angle += 10 * Global().delta_time
        v = vector.from_size_and_angle(40, to_radians(self.camera_angle))
        Camera().eye = np.array([v[0], 10, v[1]])
        Camera().target = np.array([0, 0, 0])

    def update(self) -> None:
        if KeyListener().is_key_pressed(GLUT_KEY_UP):
            self.tank.move_forward()
        if KeyListener().is_key_pressed(GLUT_KEY_DOWN):
            self.tank.move_backward()
        if KeyListener().is_key_pressed(GLUT_KEY_LEFT):
            self.tank.turn_left()
        if KeyListener().is_key_pressed(GLUT_KEY_RIGHT):
            self.tank.turn_right()
        if KeyListener().is_key_pressed(b'q'):
            self.tank.turn_base_left()
        if KeyListener().is_key_pressed(b'w'):
            self.tank.turn_base_right()
        if KeyListener().is_key_pressed(b'a'):
            self.tank.turn_cannon_up()
        if KeyListener().is_key_pressed(b's'):
            self.tank.turn_cannon_down()
        if KeyListener().is_key_first_pressed(b' '):
            self.tank.spawn_bullet()
        if KeyListener().is_key_first_pressed(b'z'):
            self.tank.increase_bullet_speed()
        if KeyListener().is_key_first_pressed(b'x'):
            self.tank.decrease_bullet_speed()

        self.ground.update()
        self.wall.update()
        self.tank.update()

        for obj in self.scene_objects:
            obj.update()

        self.rotate_camera_around()

        # print(self.aabb.check_collision(self.ground.collider))

    def draw(self) -> None:
        self.ground.draw()
        self.wall.draw()
        self.tank.draw()

        for obj in self.scene_objects:
            obj.draw()

