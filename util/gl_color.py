import numpy as np
from OpenGL.GL import *


class GlColor:
    def __init__(self):
        self.color = np.array([0, 0, 0, 0])

    @staticmethod
    def from_color(red: int, green: int, blue: int, alpha: int):
        color = GlColor()
        color.color = np.array([red / 255, green / 255, blue / 255, alpha / 255])
        return color

    @staticmethod
    def white_color():
        return GlColor.from_color(255, 255, 255, 255)

    @staticmethod
    def black_color():
        return GlColor.from_color(0, 0, 0, 255)

    @staticmethod
    def dark_gray_color():
        return GlColor.from_color(64, 64, 64, 255)

    @staticmethod
    def red_color():
        return GlColor.from_color(255, 0, 0, 255)

    @staticmethod
    def green_color():
        return GlColor.from_color(0, 255, 0, 255)

    @staticmethod
    def blue_color():
        return GlColor.from_color(0, 0, 255, 255)

    @staticmethod
    def yellow_color():
        return GlColor.from_color(0, 255, 255, 255)

    @staticmethod
    def magenta_color():
        return GlColor.from_color(255, 0, 255, 255)

    @staticmethod
    def cyan_color():
        return GlColor.from_color(255, 255, 0, 255)

    def red(self) -> float:
        return self.color[0]

    def green(self) -> float:
        return self.color[1]

    def blue(self) -> float:
        return self.color[2]

    def alpha(self) -> float:
        return self.color[3]

    def gl_set(self):
        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])

