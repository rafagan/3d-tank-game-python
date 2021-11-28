import numpy as np

from game.world import World
from primitive.box import Box
from primitive.idrawable import IDrawable
from primitive.plane import Plane
from util.gl_color import GlColor
from OpenGL.GL import *

from util.math.collision import AABB, ICollidable, ICollider


class Ground(IDrawable, ICollidable):
    def __init__(self):
        self.position = np.array([0, 0, 0])
        self.grid_width = 50
        self.grid_depth = 25
        self.planes = []
        self.collider = AABB()

        colors = [
            GlColor.white_color(),
            GlColor.black_color(),
            GlColor.dark_gray_color(),
            GlColor.red_color(),
            GlColor.green_color(),
            GlColor.blue_color(),
            GlColor.yellow_color(),
            GlColor.magenta_color(),
            GlColor.cyan_color(),
        ]

        current_color_index = 0
        for i in range(self.grid_depth):
            for j in range(self.grid_width):
                plane = Plane()
                plane.color = colors[current_color_index]
                self.planes.append(plane)
                current_color_index = (current_color_index + 1) % len(colors)

        # World().collidable_with_bullet.append(self)

    def update(self) -> None:
        self.collider.update(self.position, self.grid_width, 1, self.grid_depth)

    def draw(self) -> None:
        distance = 1
        start_x = -distance * self.grid_width / 2.0
        start_z = -distance * self.grid_depth / 2.0

        for i in range(self.grid_depth):
            for j in range(self.grid_width):
                glPushMatrix()
                glTranslatef(
                    self.position[0] + start_x + distance * j,
                    self.position[1],
                    self.position[2] + start_z + distance * i
                )
                self.planes[j + i * self.grid_depth].draw()
                glPopMatrix()

    def get_collider(self) -> ICollider:
        return self.collider

    def has_collision_with(self, other: ICollidable) -> bool:
        return self.collider.check_collision(other.get_collider())

    def on_collision_enter(self, other: ICollidable) -> None:
        ...
