from pygrunner.core import Layer
from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.tiles.base import Tile


class Ladder(Tile):
    name = ""
    animations = {}
    initial_stock = 100
    layer = Layer.background

    @classmethod
    def create(cls, sprite_loader):
        """
        Creates a game object and assigns proper components
        """
        tile = super().create(sprite_loader)
        tile.physics.solid = False
        tile.physics.platform = True

        return tile


@Factory.register
class RedLadder(Ladder):
    name = "Red Ladder"
    animations = {'idle': [SpriteInfo('packed', 'red_ladder', 21, 19)]}
