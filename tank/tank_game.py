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
        self.ground = None
        self.wall = None
        self.tank = None
        self.scene_objects = []

        self.camera_angle = 180

    def init(self) -> None:
        self.ground = Ground()
        self.wall = Wall()
        self.tank = Tank()

        tank_start_x = -self.ground.grid_width / 2 + self.tank.width / 2
        self.tank.position = np.array([tank_start_x, 1.0, 0.0])
        Camera().eye = np.array([tank_start_x - 10, 3.0, 0.0])
        Camera().target = Camera().eye + np.array([Camera().look_at_magnitude, 0.0, 0.0])
        self.create_scene_objects()

        # Top view
        # Camera().eye = np.array([0.0, 50.0, 0.1])
        # Camera().target = np.array([0.0, 0.0, 0.0])

        # Back View
        # Camera().eye = np.array([0.0, 5.0, -35.0])
        # Camera().target = np.array([0.0, 10.0, 0.0])

        # Left View
        # Camera().eye = np.array([-45.0, 5.0, -10.0])
        # Camera().target = np.array([0.0, 10.0, 0.0])

    def create_scene_objects(self):
        amount_x = 10
        amount_z = 4
        distance_x = self.ground.grid_width / amount_x
        distance_z = self.ground.grid_depth / amount_z
        start_x = -self.ground.grid_width / 2.0
        start_z = -self.ground.grid_depth / 2.0

        for i in range(11, 13):  # TODO: 40
            self.scene_objects.append(SceneObject(
                SceneObjectType.FRIEND if i % 2 == 0 else SceneObjectType.ENEMY,
                np.array([
                    start_x + distance_x * (i % amount_x),
                    2.5,
                    start_z + distance_z * (i // amount_x)
                ]),
                np.array([4, 4, 4])
            ))

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

        destroyed_objs = []
        for i, obj in enumerate(self.scene_objects):
            obj.update()
            if obj.is_dead:
                print(obj.type)
                destroyed_objs.append(i)

        if len(destroyed_objs) > 0:
            self.destroy_scene_objects(set(destroyed_objs))

        self.rotate_camera_around()

    def destroy_scene_objects(self, destroyed: set[int]) -> None:
        items = []
        for i, item in enumerate(self.scene_objects):
            if i not in destroyed:
                items.append(item)
            else:
                World().collidable_with_bullet.remove(item)

        self.scene_objects = items

    def draw(self) -> None:
        self.ground.draw()
        self.wall.draw()
        self.tank.draw()

        for obj in self.scene_objects:
            obj.draw()
