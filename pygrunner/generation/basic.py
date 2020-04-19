from pygrunner.core.level import Level
from pygrunner.gamedata.recipes.tiles.blocks import SnowyDirtTop, SnowyDirtMiddle
from pygrunner.generation import textprefabs, tmxprefabs
import random
from pygrunner import tmx


def generate_level(game):
    width = 16000
    height = 16000
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


def prefab_based(game):
    factory = game.factory
    loader = tmx.TmxLoader(factory)

    prefabs = [prefab.loading_set(loader.load_map(prefab.name)) for prefab in tmxprefabs.prefabs]
    random.shuffle(prefabs)
    total_width = sum((prefab.level.width for prefab in prefabs))
    total_height = max((prefab.level.height for prefab in prefabs)) * 4
    new_level = Level("TmxGen", total_width + 32, total_height)
    world_x = 0
    world_y = int(total_height / 2)
    for prefab in prefabs:
        prefab_width = prefab.level.width
        prefab_height = prefab.level.height
        if prefab.anchor_type == tmxprefabs.AnchorType.Grounded:
            offset_y = world_y - prefab_height
        elif prefab.anchor_type == tmxprefabs.AnchorType.Underground:
            offset_y = world_y - 32
        else:
            print("BUG")
            offset_y = world_y

        for static in prefab.level.statics:
            tx = world_x + static.location.x
            ty = offset_y + static.location.y
            static.location.level = new_level
            static.location.set(tx, ty)
            new_level.add_static(static)

        for game_object in prefab.level.game_objects:
            tx = world_x + game_object.location.x
            ty = offset_y + game_object.location.y
            game_object.location.level = new_level
            game_object.location.set(tx, ty)
            new_level.add_game_object(game_object)

        world_x += prefab_width

    return new_level


def text_based(game):
    factory = game.factory
    prefabs = [textprefabs.Bridge, textprefabs.Ravine, textprefabs.SmallBuilding, textprefabs.TwoStoryBuilding]
    total_width = sum((prefab.get_width() for prefab in prefabs)) * 32
    total_height = max((prefab.get_height() for prefab in prefabs)) * 128
    level = Level("TextGen", total_width + 32, total_height)
    random.shuffle(prefabs)
    world_x = 0
    world_y = int(total_height / 2)
    for prefab in prefabs:
        prefab_width = prefab.get_width()
        prefab_height = prefab.get_height()
        if prefab.anchor_type == textprefabs.AnchorType.Grounded:
            offset_y = world_y - (prefab_height * 32)
        elif prefab.anchor_type == textprefabs.AnchorType.Underground:
            offset_y = world_y - 32
        else:
            print("BUG")
            offset_y = world_y

        for y in range(prefab_height):
            for x in range(prefab_width):
                char_link = prefab.value[y][x]
                recipe_name = prefab.links.get(char_link)
                tile = factory.get_or_create(recipe_name)
                tx = world_x + (x * 32)
                ty = offset_y + (y * 32)
                tile.location.set(tx, ty)
                level.add_static(tile)

        world_x += (prefab_width * 32)

    return level
