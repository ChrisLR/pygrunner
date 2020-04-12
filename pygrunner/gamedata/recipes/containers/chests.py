from pygrunner.core.spriteinfo import SpriteInfo
from pygrunner.gamedata.factory import Factory
from pygrunner.gamedata.recipes.containers.base import Container


@Factory.register
class BrownChest(Container):
    name = "Brown Chest"
    animations = {'idle': [SpriteInfo('packed', 'brown_chest', 23, 18)]}
