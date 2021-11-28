import random

import numpy as np

from game.world import World
from primitive.box import Box
from primitive.idrawable import IDrawable
from util.gl_color import GlColor
from OpenGL.GL import *

from util.math.collision import AABB, ICollider, ICollidable


class Wall(IDrawable, ICollidable):
    def __init__(self):
        self.grid_width = 50
        self.grid_height = 15
        self.position = np.array([0, self.grid_height / 2 + 0.5, 0])
        self.cubes = []
        self.collider = AABB()

        colors = [
            GlColor.white_color(),
            GlColor.black_color(),
            GlColor.blue_color()
        ]

        current_color_index = 0
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                cube = Box()
                cube.colors = [colors[current_color_index]] * 6
                self.cubes.append(cube)
                current_color_index = random.Random().randrange(0, 3, 1)

        World().collidable_with_bullet.append(self)

    def update(self) -> None:
        self.collider.update(self.position, self.grid_width, self.grid_height, 1)

    def draw(self) -> None:
        distance = 1
        start_x = -distance * self.grid_width / 2.0
        start_y = -distance * self.grid_height / 2.0

        for i in range(self.grid_height):
            for j in range(self.grid_width):
                glPushMatrix()
                glTranslatef(
                    self.position[0] + start_x + distance * j,
                    self.position[1] + start_y + distance * i,
                    self.position[2]
                )
                self.cubes[j + i * self.grid_height].draw()
                glPopMatrix()

    def get_collider(self) -> ICollider:
        return self.collider

    def has_collision_with(self, other: ICollidable) -> bool:
        return self.collider.check_collision(other.get_collider())

    def on_collision_enter(self, other: ICollidable) -> None:
        ...
