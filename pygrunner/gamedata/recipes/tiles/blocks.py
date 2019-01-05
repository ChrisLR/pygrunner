from pygrunner.core import Layer
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.tiles.base import Tile


class Block(Tile):
    name = ""
    animations = {}
    initial_stock = 200
    layer = Layer.foreground


@Factory.register
class RedBlockTop(Block):
    name = "Red Block Top"
    animations = {'idle': [SpriteInfo('packed', 'red_block_top', 8, 0)]}


@Factory.register
class RedBlockMiddle(Block):
    name = "Red Block Top"
    animations = {'idle': [SpriteInfo('packed', 'red_block_middle', 9, 0)]}
