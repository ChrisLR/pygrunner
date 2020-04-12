from pygrunner.core import Layer
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.tiles.base import Tile


class BlockShadow(Tile):
    name = ""
    animations = {}
    initial_stock = 200
    layer = Layer.background

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        tile = super().create(sprite_loader)
        tile.physics.solid = False

        return tile


@Factory.register
class RedBlockTopShadow(BlockShadow):
    name = "Red Block Top Shadow"
    animations = {'idle': [SpriteInfo('packed', 'red_block_top_shadow', 9, 0)]}


@Factory.register
class RedBlockMiddleShadow(BlockShadow):
    name = "Red Block Middle Shadow"
    animations = {'idle': [SpriteInfo('packed', 'red_block_middle_shadow', 8, 0)]}


@Factory.register
class BlueBlockTopShadow(BlockShadow):
    name = "Blue Block Top Shadow"
    animations = {'idle': [SpriteInfo('packed', 'blue_block_top_shadow', 9, 1)]}


@Factory.register
class BlueBlockMiddleShadow(BlockShadow):
    name = "Blue Block Middle Shadow"
    animations = {'idle': [SpriteInfo('packed', 'blue_block_middle_shadow', 8, 1)]}


@Factory.register
class BlackBlockTopShadow(BlockShadow):
    name = "Black Block Top Shadow"
    animations = {'idle': [SpriteInfo('packed', 'black_block_top_shadow', 9, 2)]}


@Factory.register
class BlackBlockMiddleShadow(BlockShadow):
    name = "Black Block Middle Shadow"
    animations = {'idle': [SpriteInfo('packed', 'black_block_middle_shadow', 8, 2)]}



@Factory.register
class RockyDirtTopShadow(BlockShadow):
    name = "Rocky Dirt Top Shadow"
    animations = {'idle': [SpriteInfo('packed', 'rocky_dirt_top_shadow', 9, 11)]}


@Factory.register
class RockyDirtMiddleShadow(BlockShadow):
    name = "Rocky Dirt Middle Shadow"
    animations = {'idle': [SpriteInfo('packed', 'rocky_dirt_middle_shadow', 8, 11)]}


@Factory.register
class OldBridgeTopShadow(BlockShadow):
    name = "Old Bridge Top Shadow"
    animations = {'idle': [SpriteInfo('packed', 'old_bridge_top_shadow', 9, 13)]}


@Factory.register
class OldBridgeMiddleShadow(BlockShadow):
    name = "Old Bridge Middle Shadow"
    animations = {'idle': [SpriteInfo('packed', 'old_bridge_middle_shadow', 8, 13)]}
