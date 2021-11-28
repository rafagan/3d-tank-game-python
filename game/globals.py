import numpy as np

from util.decorator.singleton import singleton
from util.gl_color import GlColor


@singleton
class Global:
    def __init__(self):
        self.clear_color = GlColor.dark_gray_color()
        self.default_color = GlColor.white_color()

        self.window_title = '3D Tank Game'
        self.window_default_width = 1024
        self.window_default_height = 768
        self.window_width = self.window_default_width
        self.window_height = self.window_default_height

        self.frame_rate = 16
        self.goal_rate = 1.0 / self.frame_rate
        self.delta_time = 0

        self.gravity = np.array([0, -10, 0])

    def aspect_ratio(self):
        return self.window_width / self.window_height
