from pygrunner.core import Layer
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.tiles.base import Tile


class Door(Tile):
    name = ""
    animations = {}
    initial_stock = 200
    layer = Layer.middle


@Factory.register
class GrayRoundDoor(Door):
    name = "Gray Round Door"
    animations = {'idle': [SpriteInfo('packed', 'gray_round_door', 30, 26)]}