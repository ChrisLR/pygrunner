import os

import pyglet


class SpriteLoader(object):
    def __init__(self):
        res_dir = str(os.path.dirname(__file__).split('pygrunner')[0]) + "pygrunner/pygrunner/client/graphics/sidescroller"
        pyglet.resource.path = [res_dir]
        pyglet.resource.reindex()
        self.spritesheets = None

    def get_by_name(self, name):
        return self.spritesheets.get(name)

    def load_spritesheets(self, file_names):
        """
        Loads and initialize spritesheets
        :param file_names: File names including extension of spritesheets to load
        """
        images = [(file_name.split(".")[0], file_name) for file_name in file_names]
        self.spritesheets = {
            name: SpriteSheet(name, path) for name, path in images
        }


class SpriteSheet(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.image = pyglet.resource.image(path)
        self.image_grid = self._load_image_grid(self.image)
        self.region_names = {}

    @staticmethod
    def _load_image_grid(image):
        rows = int(image.height / 16)
        cols = int(image.width / 16)

        return pyglet.image.ImageGrid(image, rows, cols, 16, 16)

    def get_region_by_name(self, name):
        region_tuple = self.region_names.get(name)
        if region_tuple is not None:
            return self.image_grid[region_tuple]

        return None

    def get_region(self, row, col):
        return self.image_grid[row, col]

    def set_region_name(self, name, row, col):
        self.region_names[name] = (row, col)
