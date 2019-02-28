import math


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

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)
        game_object.location.level = self

    def add_static(self, static_object):
        rectangle = static_object.size.rectangle
        self.statics.append(static_object)
        self.static_collision_map.add_collider(static_object, rectangle)
        static_object.location.level = self

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
        self._collision_map = [[None for _ in range(height)] for _ in range(width)]
        self.width = width
        self.height = height

    def add_collider(self, collider, rectangle):
        for x in range(rectangle.left, rectangle.right):
            for y in range(rectangle.top, rectangle.bottom):
                self._collision_map[x][y] = collider

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
        for x in range(rectangle.left, rectangle.right):
            for y in range(rectangle.top, rectangle.bottom):
                self._collision_map[x][y] = None
