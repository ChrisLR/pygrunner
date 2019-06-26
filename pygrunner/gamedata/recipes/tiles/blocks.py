from pygrunner.core import Layer
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.tiles.base import Tile


class Block(Tile):
    name = ""
    animations = {}
    initial_stock = 200
    layer = Layer.middle


@Factory.register
class RedBlockTop(Block):
    name = "Red Block Top"
    animations = {'idle': [SpriteInfo('packed', 'red_block_top', 18, 0)]}


@Factory.register
class RedBlockMiddle(Block):
    name = "Red Block Middle"
    animations = {'idle': [SpriteInfo('packed', 'red_block_middle', 17, 0)]}


@Factory.register
class RockyDirtTop(Block):
    name = "Rocky Dirt Top"
    animations = {'idle': [SpriteInfo('packed', 'rocky_dirt_top', 18, 10)]}


@Factory.register
class RockyDirtMiddle(Block):
    name = "Rocky Dirt Middle"
    animations = {'idle': [SpriteInfo('packed', 'rocky_dirt_middle', 17, 10)]}


@Factory.register
class OldBridgeTop(Block):
    name = "Old Bridge Top"
    animations = {'idle': [SpriteInfo('packed', 'old_bridge_top', 18, 12)]}


@Factory.register
class OldBridgeMiddle(Block):
    name = "Old Bridge Middle"
    animations = {'idle': [SpriteInfo('packed', 'old_bridge_middle', 17, 12)]}
