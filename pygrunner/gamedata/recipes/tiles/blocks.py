from pyg2d.core import Layer
from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory
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
class BlueBlockTop(Block):
    name = "Blue Block Top"
    animations = {'idle': [SpriteInfo('packed', 'blue_block_top', 18, 1)]}


@Factory.register
class BlueBlockMiddle(Block):
    name = "Blue Block Middle"
    animations = {'idle': [SpriteInfo('packed', 'blue_block_middle', 17, 1)]}


@Factory.register
class BlackBlockTop(Block):
    name = "Black Block Top"
    animations = {'idle': [SpriteInfo('packed', 'black_block_top', 18, 1)]}


@Factory.register
class BlackBlockMiddle(Block):
    name = "Black Block Middle"
    animations = {'idle': [SpriteInfo('packed', 'black_block_middle', 17, 1)]}


@Factory.register
class YellowBlockTop(Block):
    name = "Yellow Block Top"
    animations = {'idle': [SpriteInfo('packed', 'yellow_block_top', 18, 3)]}


@Factory.register
class YellowBlockMiddle(Block):
    name = "Yellow Block Middle"
    animations = {'idle': [SpriteInfo('packed', 'yellow_block_middle', 17, 3)]}


@Factory.register
class RockyDirtTop(Block):
    name = "Rocky Dirt Top"
    animations = {'idle': [SpriteInfo('packed', 'rocky_dirt_top', 18, 11)]}


@Factory.register
class RockyDirtMiddle(Block):
    name = "Rocky Dirt Middle"
    animations = {'idle': [SpriteInfo('packed', 'rocky_dirt_middle', 17, 11)]}


@Factory.register
class SnowyDirtTop(Block):
    name = "Snowy Dirt Top"
    animations = {'idle': [SpriteInfo('packed', 'snowy_dirt_top', 18, 10)]}


@Factory.register
class SnowyDirtMiddle(Block):
    name = "Snowy Dirt Middle"
    animations = {'idle': [SpriteInfo('packed', 'snowy_dirt_middle', 17, 10)]}


@Factory.register
class OldBridgeTop(Block):
    name = "Old Bridge Top"
    animations = {'idle': [SpriteInfo('packed', 'old_bridge_top', 18, 13)]}


@Factory.register
class OldBridgeMiddle(Block):
    name = "Old Bridge Middle"
    animations = {'idle': [SpriteInfo('packed', 'old_bridge_middle', 17, 13)]}
