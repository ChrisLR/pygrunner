import json

from lxml import etree

from pygrunner.core.level import Level


class TmxLoader(object):
    def __init__(self, factory):
        self.factory = factory
        self.tileset_map = self.define_tileset_map()

    @classmethod
    def define_tileset_map(cls):
        tileset_map = {}
        with open('tmx\\platformer.tsx', 'rb') as tileset_file:
            for event, element in etree.iterparse(tileset_file):
              if element.tag == 'tile':
                  tileset_map[int(element.get('id'))] = element.get('type')

        return tileset_map

    def load_map(self, map_name):
        with open('tmx\\%s' % map_name, 'r') as map_file:
            json_level = json.load(map_file)

        new_level = Level(map_name, json_level['width'], json_level['height'])
        if json_level['renderorder'] != "left-down":
            # TODO Support multiple render orders
            raise Exception("Bad render order")

        for layer in json_level['layers']:
            if layer['name'] != 'foreground':
                # TODO We'll want to support multi layers in a more pythonic way
                continue

            layer_data = (tile_id for tile_id in layer['data'])
            layer_width = layer['width']
            layer_height = layer['height']
            # TODO Might have to support more than one tileset
            first_gid = json_level['tilesets'][0]['firstgid']
            for y in range(layer_height):
                for x in range(layer_width):
                    tile_id = next(layer_data) - first_gid
                    tile_type = self.tileset_map.get(tile_id)
                    if tile_type:
                        tile = self.factory.get_or_create(tile_type)
                        tile.location.set(x * 16, y * 16)
                        new_level.add_static(tile)

        # TODO We need to support objects, such as spawn points

        return new_level
