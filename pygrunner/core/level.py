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
        self.static_collision_map = CollisionMap()

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)

    def add_static(self, static_object):
        rectangle = static_object.size.rectangle
        self.statics.append(static_object)
        self.static_collision_map.add_collider(static_object, rectangle)

    def remove_static(self, static_object):
        rectangle = static_object.size.rectangle
        self.statics.remove(static_object)
        self.static_collision_map.remove_collider(rectangle)


class CollisionMap(object):
    """
    An object containing rectangles of static game objects for collisions
    """
    def __init__(self):
        self._collision_map = {}

    def add_collider(self, collider, rectangle):
        for x in range(rectangle.left, rectangle.right):
            for y in range(rectangle.top, rectangle.bottom):
                self._collision_map[(x, y)] = collider

    def check_collision_point(self, point):
        return self._collision_map.get((point.x, point.y))

    def check_collision_rect(self, rectangle):
        collisions = set()
        for x in range(rectangle.left, rectangle.right):
            for y in range(rectangle.top, rectangle.bottom):
                collision = self._collision_map.get((x, y))
                if collision is not None:
                    collisions.add(collision)

        return collisions

    def remove_collider(self, rectangle):
        for x in range(rectangle.left, rectangle.right):
            for y in range(rectangle.top, rectangle.bottom):
                del self._collision_map[(x, y)]
