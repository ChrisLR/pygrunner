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
            game_object = self.factory.get_or_create(tmx_object.object_type)
            game_object.location.set(tmx_object.x, tmx_object.y)
            level.add_game_object(game_object)


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
                        current_tileset = cls.get_tileset_used_by_gid(tilesets, tile_id)
                        tileset_tile = current_tileset.id_mapping.get(tile_id - current_tileset.first_gid)
                        layer_tile_data.append(tileset_tile.tile_type)
                    else:
                        layer_tile_data.append(None)
                layers.append(TmxLayer(layer_id, layer_name, layer_width, layer_height, layer_tile_data))
            elif child.tag == 'objectgroup':
                layer_id = child.attrib.get('id')
                layer_name = child.attrib.get('name')
                tmx_objects = []
                for tmx_object in child:
                    attribs = tmx_object.attrib
                    object_gid = int(attribs['gid'])
                    tileset = cls.get_tileset_used_by_gid(tilesets, object_gid)
                    object_type = tileset.id_mapping.get(object_gid - tileset.first_gid)

                    tmx_objects.append(
                        TmxObject(
                            attribs['id'], object_gid,
                            float(attribs['x']), float(attribs['y']) - 16,
                            int(attribs['width']), int(attribs['height']), object_type.tile_type))

                object_layers.append(TmxObjectLayer(layer_id, layer_name, tmx_objects))

        return TmxMap(map_width, map_height, tilesets, layers, object_layers, render_order, tile_height, tile_width)

    @classmethod
    def get_tileset_used_by_gid(cls, tilesets, gid):
        return max((tileset for tileset in tilesets if tileset.first_gid <= gid),
                   key=lambda t: t.first_gid)


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