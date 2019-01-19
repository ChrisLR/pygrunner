import json

from lxml import etree

from pygrunner.core.level import Level


class TmxLoader(object):
    def __init__(self, factory):
        self.factory = factory
        self.tileset = self.define_tileset()

    @classmethod
    def define_tileset(cls):
        return TmxTileset.from_xml('tmx\\platformer.tsx')

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

    def load_map_xml(self, map_name):
        pass


class TmxMap(object):
    def __init__(self, width, height, tilesets, layers, render_order, tile_height, tile_width):
        self.width = width
        self.height = height
        self.tilesets = tilesets
        self.layers = layers
        self.render_order = render_order
        self.tile_height = tile_height
        self.tile_width = tile_width

    @classmethod
    def from_xml(cls, xml_file_name):
        with open(xml_file_name, 'rb') as xml_file:
            tree = etree.parse(xml_file)
        root = tree.getroot()
        render_order = root.attrib.get('renderorder')
        tile_width = int(root.attrib.get('tilewidth'))
        tile_height = int(root.attrib.get('tileheight'))
        map_width = int(root.attrib.get('width'))
        map_height = int(root.attrib.get('height'))
        tilesets = []
        layers = []
        for child in root:
            if child.tag == 'tileset':
                first_gid = int(child.attrib.get('firstgid'))
                tileset_source = child.attrib.get('source')
                tmx_tileset = TmxTileset.from_xml(tileset_source)
                tmx_tileset.first_gid = first_gid
                tilesets.append(tmx_tileset)
            elif child.tag == 'layer':
                layer_id = child.attrib.get('id')
                layer_name = child.attrib.get('name')
                layer_width = int(child.attrib.get('width'))
                layer_height = int(child.attrib.get('height'))
                layer_data = child[0]
                layer_tile_data = []
                for tile_data in layer_data:
                    tile_id = tile_data.get('gid')
                    if tile_id:
                        tile_id = int(tile_id)
                        current_tileset = max(
                            (tileset for tileset in tilesets if tileset.first_gid <= tile_id),
                            key=lambda t:t.first_gid)
                        tileset_tile = current_tileset.id_mapping.get(tile_id - current_tileset.first_gid)
                        layer_tile_data.append(tileset_tile.tile_type)
                    else:
                        layer_tile_data.append(None)
                layers.append(TmxLayer(layer_id, layer_name, layer_width, layer_height, layer_tile_data))

        return TmxMap(map_width, map_height, tilesets, layers, render_order, tile_height, tile_width)


class TmxLayer(object):
    def __init__(self, layer_id, name, width, height, tiles):
        self.layer_id = layer_id
        self.name = name
        self.width = width
        self.height = height
        self.tiles = tiles


class TmxTileset(object):
    def __init__(self, tiles, id_mapping):
        self.tiles = tiles
        self.id_mapping = id_mapping
        self.first_gid = None

    @classmethod
    def from_xml(cls, xml_file_name):
        tiles = []
        id_mapping = {}
        with open(xml_file_name, 'rb') as xml_file:
            tree = etree.parse(xml_file)
        root = tree.getroot()
        for child in root:
            if not child.tag == 'tile':
                continue

            tile_id = int(child.attrib.get('id'))
            tile_type = child.attrib.get('type')
            tile = TmxTile(tile_id, tile_type)
            id_mapping[tile_id] = tile
            tiles.append(tile)

        return TmxTileset(tiles, id_mapping)


class TmxTile(object):
    __slots__ = ('tile_id', 'tile_type')

    def __init__(self, tile_id, tile_type):
        self.tile_id = tile_id
        self.tile_type = tile_type


if __name__ == '__main__':
    tmx_map = TmxMap.from_xml('simple.tmx')
    print('')