from pygrunner.core.level import Level
from pygrunner.gamedata.recipes.tiles.blocks import SnowyDirtTop, SnowyDirtMiddle


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

    return level


class ChunkProxy(object):
    def __init__(self, chunk, rectangle):
        self.chunk = chunk
        self.rectangle = rectangle

    def load(self):
        pass

    def unload(self):
        pass