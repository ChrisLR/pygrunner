from pyg2d.core import Layer
from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory
from pygrunner.gamedata.recipes.tiles.base import Tile


class Door(Tile):
    name = ""
    animations = {}
    initial_stock = 200
    layer = Layer.middle

    @classmethod
    def create(cls, sprite_loader):
        created = super().create(sprite_loader)
        created.physics.solid = False
        return created


@Factory.register
class GrayRoundDoor(Door):
    name = "Gray Round Door"
    animations = {'idle': [SpriteInfo('packed', 'gray_round_door', 30, 26)]}