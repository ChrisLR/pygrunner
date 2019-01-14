from pygrunner.core.level import Level


class TmxLoader(object):
    def __init__(self, factory):
        self.factory = factory

    @classmethod
    def load_map(cls, map_name):
        # TODO pytmx does not cut it here.
        # TODO for this project all we need
        # TODO is to get a few details about the map and know
        # TODO which type of tile is placed where
        # TODO We can probably get away with home made stuff
        # new_level = Level(map_name, tiled_map.width, tiled_map.height)
        return 'HM'


if __name__ == '__main__':
    TmxLoader.load_map('simple.tmx')
