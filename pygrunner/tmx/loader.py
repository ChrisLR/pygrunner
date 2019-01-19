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
        map_file_name = "tmx\\%s.tmx" % map_name
        tmx_map = TmxMap.from_xml(map_file_name)
        level = Level(map_name, tmx_map.pixel_width, tmx_map.pixel_height)
        for layer in tmx_map.layers:

    def _handle_tile_layer(self, layer, level):
        pass

    def _handle_object_layer(self, layer, level):
        pass


class TmxMap(object):
    def __init__(self, width, height, tilesets, layers, object_layers, render_order, tile_height, tile_width):
        self.width = width
        self.height = height
        self.tilesets = tilesets
        self.layers = layers
        self.object_layers = object_layers
        self.render_order = render_order
        self.tile_height = tile_height
        self.tile_width = tile_width

    @property
    def pixel_width(self):
        return self.width * self.tile_width

    @property
    def pixel_height(self):
        return self.height * self.tile_height

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
        object_layers = []
        for child in root:
            if child.tag == 'tileset':
                first_gid = int(child.attrib.get('firstgid'))
                tileset_source = "tmx\\" + child.attrib.get('source')
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
            elif child.tag == 'objectgroup':
                layer_id = child.attrib.get('id')
                layer_name = child.attrib.get('name')
                tmx_objects = [
                    TmxObject(
                        tmx_object.attrib['object_id'],
                        tmx_object.attrib['object_gid'],
                        tmx_object.attrib['x'],
                        tmx_object.attrib['y'],
                        tmx_object.attrib['width'],
                        tmx_object.attrib['height'])
                    for tmx_object in child]
                object_layers.append(TmxObjectLayer(layer_id, layer_name, tmx_objects))

        return TmxMap(map_width, map_height, tilesets, layers, object_layers, render_order, tile_height, tile_width)

    def get_tileset_used_by_gid(self):
        pass


class TmxLayer(object):
    def __init__(self, layer_id, name, width, height, tiles):
        self.layer_id = layer_id
        self.name = name
        self.width = width
        self.height = height
        self.tiles = tiles


class TmxObjectLayer(object):
    def __init__(self, layer_id, name, objects):
        self.layer_id = layer_id
        self.name = name
        self.objects = objects


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


class TmxObject(object):
    __slots__ = ('object_id', 'object_gid', 'x', 'y', 'width', 'height', 'object_type')

    def __init__(self, object_id, object_gid, x, y, width, height, object_type):
        self.object_id = object_id
        self.object_gid = object_gid
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.object_type = object_type


if __name__ == '__main__':
    tmx_map = TmxMap.from_xml('simple.tmx')
    print('')