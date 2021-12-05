import numpy as np
from OpenGL.GL import *

from game.asset_manager import AssetManager
from game.world import World
from primitive.box import Box
from primitive.idrawable import IDrawable
from tank.game_manager import GameManager
from util.math.collision import AABB, ICollider, ICollidable


class Wall(IDrawable, ICollidable):
    def __init__(self):
        self.grid_depth = 25
        self.grid_height = 15
        self.position = np.array([0, self.grid_height / 2 + 0.5, 0])
        self.cubes = []
        self.cube_colliders = []
        self.collider = AABB()
        self.texture_id = AssetManager().load_texture('texture_atlas.jpg')

        for i in range(self.grid_height):
            for j in range(self.grid_depth):
                cube = Box(texture_range=np.array([0.0, 0.5, 0.0, 0.5]))
                self.cubes.append(cube)

        distance = 1
        start_z = -distance * self.grid_depth / 2.0
        start_y = -distance * self.grid_height / 2.0

        for i in range(self.grid_height):
            for j in range(self.grid_depth):
                aabb = AABB()
                aabb.position = np.array([
                    self.position[0],
                    self.position[1] + start_y + distance * i,
                    self.position[2] + start_z + distance * j
                ])
                self.cube_colliders.append(aabb)

        World().collidable_with_bullet.append(self)

    def update(self) -> None:
        self.collider.update(self.position, 1, self.grid_height, self.grid_depth)

    def draw(self) -> None:
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        for i in range(self.grid_height):
            for j in range(self.grid_depth):
                index = j + i * self.grid_depth
                cube = self.cubes[index]
                if cube is None:
                    continue

                glPushMatrix()
                glTranslatef(
                    self.cube_colliders[index].position[0],
                    self.cube_colliders[index].position[1],
                    self.cube_colliders[index].position[2]
                )
                cube.draw()
                glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, 0)
        # self.collider.draw()

    def get_collider(self) -> ICollider:
        return self.collider

    def has_collision_with(self, other: ICollidable) -> bool:
        return self.collider.check_collision(other.get_collider())

    def on_collision_enter(self, other: ICollidable) -> None:
        from tank.bullet import Bullet

        if isinstance(other, Bullet):
            destroyed_tiles = []
            for i, aabb in enumerate(self.cube_colliders):
                if aabb is None:
                    continue
                if aabb.check_collision(other.get_collider()):
                    destroyed_tiles.append(i - 1 - self.grid_depth)
                    destroyed_tiles.append(i - self.grid_depth)
                    destroyed_tiles.append(i + 1 - self.grid_depth)
                    destroyed_tiles.append(i - 1)
                    destroyed_tiles.append(i)
                    destroyed_tiles.append(i + 1)
                    destroyed_tiles.append(i - 1 + self.grid_depth)
                    destroyed_tiles.append(i + self.grid_depth)
                    destroyed_tiles.append(i + 1 + self.grid_depth)
                    other.kill()
                    break

            self.destroy_wall_tiles(set(destroyed_tiles))

    def destroy_wall_tiles(self, destroyed_indexes: set[int]) -> None:
        for i in destroyed_indexes:
            if i < 0 or i > self.grid_depth * self.grid_height:
                continue
            self.cubes[i] = None
            self.cube_colliders[i] = None
            GameManager().score_killed_wall_tile()
