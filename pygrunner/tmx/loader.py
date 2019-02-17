from pygrunner.core.level import Level
from pygrunner.tmx.tmxobjects import TmxMap


class TmxLoader(object):
    def __init__(self, factory):
        self.factory = factory

    def load_map(self, map_name):
        map_file_name = "tmx\\%s.tmx" % map_name
        tmx_map = TmxMap.from_xml(map_file_name)
        level = Level(map_name, tmx_map.pixel_width, tmx_map.pixel_height)
        for layer in tmx_map.layers:
            self._handle_tile_layer(layer, level)

        for layer in tmx_map.object_layers:
            self._handle_object_layer(layer, level)

        return level

    def _handle_tile_layer(self, layer, level):
        layer_data = (tile for tile in layer.tiles)
        for y in range(layer.height):
            for x in range(layer.width):
                tile_type = next(layer_data)
                if tile_type:
                    tile = self.factory.get_or_create(tile_type)
                    tile.location.set(x * 16, y * 16)
                    level.add_static(tile)

    def _handle_object_layer(self, layer, level):
        for tmx_object in layer.objects:
            game_object = self.factory.get_or_create(
                tmx_object.object_type, tmx_object.properties)
            game_object.location.set(tmx_object.x, tmx_object.y)
            level.add_game_object(game_object)
