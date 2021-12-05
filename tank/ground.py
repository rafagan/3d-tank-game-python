import numpy as np
from OpenGL.GL import *

from game.asset_manager import AssetManager
from game.world import World
from primitive.idrawable import IDrawable
from primitive.plane import Plane
from tank.game_manager import GameManager
from util.math.collision import AABB, ICollidable, ICollider


class Ground(IDrawable, ICollidable):
    def __init__(self):
        self.position = np.array([0, 0, 0])
        self.grid_width = 50
        self.grid_depth = 25
        self.planes = []
        self.plane_colliders = []
        self.collider = AABB()
        self.texture_id = AssetManager().load_texture('texture_atlas.jpg')

        for i in range(self.grid_depth):
            for j in range(self.grid_width):
                plane = Plane(texture_range=np.array([0.5, 1.0, 0.0, 0.5]))
                self.planes.append(plane)

        distance = 1
        start_x = -distance * self.grid_width / 2.0
        start_z = -distance * self.grid_depth / 2.0
        for i in range(self.grid_depth):
            for j in range(self.grid_width):
                aabb = AABB()
                aabb.position = np.array([
                    self.position[0] + start_x + distance * j,
                    self.position[1],
                    self.position[2] + start_z + distance * i
                ])
                self.plane_colliders.append(aabb)

        World().collidable_with_bullet.append(self)

    def update(self) -> None:
        self.collider.update(self.position, self.grid_width, 1, self.grid_depth)

    def draw(self) -> None:
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        for i in range(self.grid_depth):
            for j in range(self.grid_width):
                index = j + i * self.grid_width
                plane = self.planes[index]
                if plane is None:
                    continue

                glPushMatrix()
                glTranslatef(
                    self.plane_colliders[index].position[0],
                    self.plane_colliders[index].position[1],
                    self.plane_colliders[index].position[2]
                )
                self.planes[index].draw()
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
            for i, aabb in enumerate(self.plane_colliders):
                if aabb is None:
                    continue
                if aabb.check_collision(other.get_collider()):
                    destroyed_tiles.append(i)
                    other.kill()
                    GameManager().score_killed_ground_tile()
                    break

            self.destroy_tiles(set(destroyed_tiles))

    def destroy_tiles(self, destroyed_indexes: set[int]) -> None:
        for i in destroyed_indexes:
            self.planes[i] = None
            self.plane_colliders[i] = None

