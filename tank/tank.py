import numpy as np
from OpenGL.GL import *

from game.camera import Camera
from game.globals import Global
from game.world import World
from primitive.box import Box
from primitive.cylinder import Cylinder
from primitive.idrawable import IDrawable
from tank.bullet import Bullet
from tank.game_manager import GameManager
from util.gl_color import GlColor
from util.math import vector, to_radians
from util.math.collision import ICollidable, ICollider, AABB


class Tank(IDrawable, ICollidable):
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.start_angle = 0
        self.angle = 0
        self.width = 3
        self.height = 1
        self.depth = 2

        self.linear_speed = 2.5
        self.angular_speed = 45.0
        self.bullet_speed = 10.0

        self.base_angle = 0.0
        self.cannon_angle = 45.0
        self.base_offset = np.array([0, 1.25, 0])
        self.cannon_offset = np.array([0, 1, 0])

        self.mesh = Box()
        self.mesh.colors = [GlColor.black_color()] * 6
        self.base_mesh = Cylinder()
        self.base_mesh.color = GlColor.yellow_color()
        self.cannon_mesh = Cylinder()
        self.cannon_mesh.colors = GlColor.cyan_color()

        self.bullets = []

        self.collider = AABB()
        World().collidable_with_bullet.append(self)

    def __move(self, sense) -> None:
        linear_velocity_xz = vector.from_size_and_angle(
            sense * self.linear_speed, to_radians(self.current_angle())
        )
        offset_xz = linear_velocity_xz * Global().delta_time
        self.position += np.array([offset_xz[0], 0, offset_xz[1]])

        offset = self.linear_speed * Global().delta_time * sense
        Camera().move(offset)

    def __turn(self, clock_sense) -> None:
        angular_velocity = self.angular_speed * clock_sense
        delta = angular_velocity * Global().delta_time
        self.angle += delta
        Camera().turn(-delta)

    def __turn_base(self, clock_sense) -> None:
        angular_velocity = self.angular_speed * clock_sense
        delta = angular_velocity * Global().delta_time
        self.base_angle += delta

    def __turn_cannon(self, clock_sense) -> None:
        angular_velocity = self.angular_speed * clock_sense
        delta = angular_velocity * Global().delta_time
        self.cannon_angle += delta

    def __change_bullet_speed(self, amount):
        self.bullet_speed += amount
        print(f'Bullet speed changed: {self.bullet_speed}')

    def move_forward(self) -> None:
        self.__move(1)

    def move_backward(self) -> None:
        self.__move(-1)

    def turn_left(self) -> None:
        self.__turn(-1)

    def turn_right(self) -> None:
        self.__turn(1)

    def turn_base_left(self) -> None:
        self.__turn_base(-1)

    def turn_base_right(self) -> None:
        self.__turn_base(1)

    def turn_cannon_up(self) -> None:
        self.__turn_cannon(-1)

    def turn_cannon_down(self) -> None:
        self.__turn_cannon(1)

    def increase_bullet_speed(self):
        self.__change_bullet_speed(1)

    def decrease_bullet_speed(self):
        self.__change_bullet_speed(-1)

    def current_angle(self) -> float:
        return self.angle + self.start_angle
    
    def current_cannon_angle(self) -> float:
        return self.current_angle() + self.base_angle

    def spawn_bullet(self):
        self.bullets.append(Bullet(
            self.position + self.base_offset,
            vector.rotate(
                self.get_forward_cannon_direction(),
                to_radians(self.cannon_angle - 90),
                self.get_strafe_cannon_axis()
            ),
            self.bullet_speed
        ))

    def update(self) -> None:
        destroyed_bullets = []
        for i, bullet in enumerate(self.bullets):
            if bullet.lifetime < bullet.max_lifetime:
                bullet.update()
            else:
                destroyed_bullets.append(i)

        self.destroy_bullets(set(destroyed_bullets))
        self.check_collisions_with_bullets()

        self.collider.update(self.position, self.width + 1, self.height, self.depth + 1)

    def check_collisions_with_bullets(self) -> None:
        for i, bullet in enumerate(self.bullets):
            for collidable in World().collidable_with_bullet:
                if bullet.has_collision_with(collidable):
                    bullet.on_collision_enter(collidable)
                    collidable.on_collision_enter(bullet)

    def destroy_bullets(self, destroyed_bullets: set[int]) -> None:
        items = []
        for i, bullet in enumerate(self.bullets):
            if i not in destroyed_bullets:
                items.append(bullet)

        self.bullets = items

    def get_forward_cannon_direction(self) -> np.array:
        direction_xz = vector.from_size_and_angle(1, to_radians(self.current_cannon_angle()))
        return np.array([direction_xz[0], 0, direction_xz[1]])

    def get_strafe_cannon_axis(self) -> np.array:
        return np.cross(
            np.array([0, 1, 0]),
            self.get_forward_cannon_direction(),
        )

    def draw(self) -> None:
        for bullet in self.bullets:
            bullet.draw()

        glPushMatrix()  # 1

        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(-self.angle, 0, 1, 0)

        glPushMatrix()  # 2

        glTranslatef(self.base_offset[0], self.base_offset[1], self.base_offset[2])
        glRotatef(-self.base_angle, 0, 1, 0)
        glPushMatrix()
        glScalef(1.0, 1.25, 1.0)
        self.base_mesh.draw()
        glPopMatrix()

        glPushMatrix()  # 3
        glRotatef(-self.cannon_angle, 0, 0, 1)
        glTranslatef(self.cannon_offset[0], self.cannon_offset[1], self.cannon_offset[2])
        glScalef(0.75, 0.75, 0.75)
        self.cannon_mesh.draw()
        glPopMatrix()  # 3

        glPopMatrix()  # 2

        glScalef(self.width, self.height, self.depth)
        self.mesh.draw()

        glPopMatrix()  # 1

        self.collider.draw()

    def get_collider(self) -> ICollider:
        return self.collider

    def has_collision_with(self, other: ICollidable) -> bool:
        return self.collider.check_collision(other.get_collider())

    def on_collision_enter(self, other: ICollidable) -> None:
        from tank.bullet import Bullet

        if isinstance(other, Bullet):
            other.kill()
            GameManager().killed_myself()
