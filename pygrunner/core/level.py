import math
from pygrunner.core import util


class Level(object):
    """
    A container of objects and statics representing a game level.
    """
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.game_objects = []
        self.statics = []
        self.static_collision_map = CollisionMap(width, height)
        self.background_image = None
        self.background_image_offset = None
        self.background_color = None

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)
        game_object.location.level = self

    def add_static(self, static_object):
        rectangle = static_object.size.rectangle
        self.statics.append(static_object)
        self.static_collision_map.add_collider(static_object, rectangle)
        static_object.location.level = self

    def replace_static(self, new_static_object):
        new_grid_point = new_static_object.location.grid_point

        def _has_same_grid(old_static_object):
            old_point = old_static_object.location.grid_point
            if old_point.x == new_grid_point.x and old_point.y == new_grid_point.y:
                return True
            return False

        swap_out = filter(_has_same_grid, (static for static in self.statics))
        for swap_obj in swap_out:
            self.statics.remove(swap_obj)
        self.add_static(new_static_object)



    def set_background_image(self, image, offset):
        self.background_image = image
        self.background_image_offset = offset

    def remove_static(self, static_object):
        rectangle = static_object.size.rectangle
        self.statics.remove(static_object)
        self.static_collision_map.remove_collider(rectangle)

    def remove_game_object(self, game_object):
        self.game_objects.remove(game_object)


class CollisionMap(object):
    """
    An object containing rectangles of static game objects for collisions
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.width_tiles = int(math.ceil(width / 32)) + 1
        self.height_tiles = int(math.ceil(height / 32)) + 1
        self._collision_map = [[None for _ in range(self.height_tiles)] for _ in range(self.width_tiles)]

    def add_collider(self, collider, rectangle):
        width_tiles = int(rectangle.width / 32)
        height_tiles = int(rectangle.height / 32)
        ox = int(rectangle.left / 32)
        oy = int(rectangle.top / 32)
        for x in range(ox, ox + width_tiles):
            for y in range(oy, oy + height_tiles):
                self._collision_map[x][y] = collider

    def check_collision(self, x, y):
        return self._collision_map[x][y]

    def check_collision_point(self, point):
        return self._collision_map[point.x][point.y]

    def check_collision_rect(self, rectangle):
        collisions = set()
        for x in range(int(rectangle.left), int(math.ceil(rectangle.right))):
            for y in range(int(rectangle.top), int(math.ceil(rectangle.bottom))):
                if x < 0 or x >= self.width:
                    continue
                if y < 0 or y >= self.height:
                    continue
                collision = self._collision_map[x][y]
                if collision is not None:
                    collisions.add(collision)

        return collisions

    def remove_collider(self, rectangle):
        width_tiles = int(rectangle.width / 32)
        height_tiles = int(rectangle.height / 32)
        ox = int(rectangle.left / 32)
        oy = int(rectangle.top / 32)
        for x in range(ox, ox + width_tiles):
            for y in range(oy, oy + height_tiles):
                self._collision_map[x][y] = None
