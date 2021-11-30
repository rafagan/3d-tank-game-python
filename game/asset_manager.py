import pygame

from game.globals import Global
from tri.tri_mesh import TriMesh
from util.decorator.singleton import singleton
from OpenGL.GL import *


@singleton
class AssetManager:
    def __init__(self):
        self.enemy_mesh = TriMesh('tree_1.tri')
        self.friend_mesh = TriMesh('dog_2.tri')

    @staticmethod
    def load_texture(file_name):
        file_path = f'{Global().resources_path}/textures/{file_name}'
        texture_surface = pygame.image.load(file_path)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", False)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB, width, height,
            0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data
        )

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return tex_id
