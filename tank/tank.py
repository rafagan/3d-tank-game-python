import numpy as np

from game.camera import Camera
from game.globals import Global
from game.world import World
from primitive.box import Box
from primitive.idrawable import IDrawable
from tank.bullet import Bullet
from util.gl_color import GlColor
from OpenGL.GL import *

from util.math import vector, to_radians
from util.math.collision import ICollidable
from window.key_listener import KeyListener


class Tank(IDrawable):
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.start_angle = 90
        self.angle = 0
        self.width = 2
        self.height = 1
        self.depth = 3

        self.linear_speed = 2.5
        self.angular_speed = 45.0
        self.bullet_speed = 10.0

        self.mesh = Box()
        self.mesh.colors = [GlColor.black_color()] * 6

        self.bullets = []

    def __move(self, sense) -> None:
        linear_velocity_xz = vector.from_size_and_angle(
            sense * self.linear_speed, to_radians(self.current_angle())
        )
        offset_xz = linear_velocity_xz * Global().delta_time
        self.position += np.array([offset_xz[0], 0, offset_xz[1]])

        offset = self.linear_speed * Global().delta_time * sense
        # Camera().move(offset)

    def __turn(self, clock_sense) -> None:
        angular_velocity = self.angular_speed * clock_sense
        delta = angular_velocity * Global().delta_time
        self.angle += delta
        # Camera().turn(delta)

    def move_forward(self) -> None:
        self.__move(1)

    def move_backward(self) -> None:
        self.__move(-1)

    def turn_left(self) -> None:
        self.__turn(-1)

    def turn_right(self) -> None:
        self.__turn(1)

    def current_angle(self) -> float:
        return self.angle + self.start_angle

    def spawn_bullet(self):
        direction_xz = vector.from_size_and_angle(1, to_radians(self.current_angle()))

        self.bullets.append(Bullet(
            self.position.copy(),
            vector.rotate(
                np.array([direction_xz[0], 0, direction_xz[1]]),
                to_radians(-45),
                np.array([1.0, 0.0, 0.0])
            ),
            self.bullet_speed
        ))

    def update(self) -> None:
        if KeyListener().is_key_first_pressed(b' '):
            self.spawn_bullet()

        for bullet in self.bullets:
            bullet.update()

        self.check_collisions_with_bullets()

    def check_collisions_with_bullets(self):
        destroyed_bullets = []
        for i, bullet in enumerate(self.bullets):
            for collidable in World().collidable_with_bullet:
                if collidable.has_collision_with(bullet):
                    bullet.on_collision_enter(collidable)
                    collidable.on_collision_enter(bullet)
                    destroyed_bullets.append(i)

        for i in destroyed_bullets:
            self.bullets.remove(i)

    def draw(self) -> None:
        for bullet in self.bullets:
            bullet.draw()

        glPushMatrix()
        glTranslatef(
            self.position[0],
            self.position[1],
            self.position[2]
        )
        glRotatef(-self.angle, 0, 1, 0)
        glScalef(self.width, self.height, self.depth)

        self.mesh.draw()
        glPopMatrix()
