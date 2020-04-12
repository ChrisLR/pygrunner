from pygrunner.core.level import Level
from pygrunner.gamedata.recipes.tiles.blocks import SnowyDirtTop, SnowyDirtMiddle
from pygrunner.tmx.loader import TmxLoader


def generate_level(game):
    width = 10240
    height = 1728
    level = Level("Test1", width, height)
    factory = game.factory
    # Generate Top Snow
    middle_y = int(height / 2)
    for x in range(0, width, 32):
        for y in range(middle_y, height, 32):
            recipe = SnowyDirtTop if y == middle_y else SnowyDirtMiddle
            tile = factory.get_or_create(recipe)
            tile.location.set(x, y)
            level.add_static(tile)

    add_prefab(game, level, 160, middle_y + 1)

    return level


def add_prefab(game, level, anchor_x, anchor_y):
    loader = TmxLoader(game.factory)
    prefab_level = loader.load_map('prefabs\\house1')

    half_prefab = int(prefab_level.height / 2)

    for tile in prefab_level.statics:
        tile.location.level = level
        tile.location.set(anchor_x + tile.location.x, anchor_y + tile.location.y - half_prefab)
        level.replace_static(tile)

    for game_object in prefab_level.game_objects:
        game_object.location.level = level
        game_object.location.set(anchor_x + game_object.location.x, anchor_y + game_object.location.y - half_prefab)
        level.add_game_object(game_object)


class ChunkProxy(object):
    def __init__(self, chunk, rectangle):
        self.chunk = chunk
        self.rectangle = rectangle

    def load(self):
        pass

    def unload(self):
        pass