import os

from game.globals import Global
from tank.tank_game import TankGame
from window.window import Window

Global().resources_path = f'{os.path.dirname(__file__)}/resources'
Window().run(TankGame())
