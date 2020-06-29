from pyg2d.core.spriteinfo import SpriteInfo
from pyg2d.gamedata import Factory
from pygrunner.gamedata.recipes.terrain.base import Terrain


@Factory.register
class Cloud1Left(Terrain):
    name = "Cloud 1 Left"
    animations = {'idle': [SpriteInfo('packed', 'cloud_1_left', 7, 30)]}


@Factory.register
class Cloud1Middle(Terrain):
    name = "Cloud 1 Middle"
    animations = {'idle': [SpriteInfo('packed', 'cloud_1_middle', 7, 31)]}


@Factory.register
class Cloud1Right(Terrain):
    name = "Cloud 1 Right"
    animations = {'idle': [SpriteInfo('packed', 'cloud_1_right', 7, 32)]}


@Factory.register
class Cloud2Left(Terrain):
    name = "Cloud 2 Left"
    animations = {'idle': [SpriteInfo('packed', 'cloud_2_left', 6, 30)]}


@Factory.register
class Cloud2Middle(Terrain):
    name = "Cloud 2 Middle"
    animations = {'idle': [SpriteInfo('packed', 'cloud_2_middle', 6, 31)]}


@Factory.register
class Cloud2Right(Terrain):
    name = "Cloud 2 Right"
    animations = {'idle': [SpriteInfo('packed', 'cloud_2_right', 6, 32)]}
