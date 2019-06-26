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
class OldBridgeTopShadow(BlockShadow):
    name = "Old Bridge Top Shadow"
    animations = {'idle': [SpriteInfo('packed', 'old_bridge_top_shadow', 9, 12)]}


@Factory.register
class OldBridgeMiddleShadow(BlockShadow):
    name = "Old Bridge Middle Shadow"
    animations = {'idle': [SpriteInfo('packed', 'old_bridge_middle_shadow', 8, 12)]}
