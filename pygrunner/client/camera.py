import pyglet

from pygrunner.core.layers import Layer
from pygrunner.core import util


class Camera(object):
    """
    This objects creates pyglet sprites as required to match the current level's objects.
    It will adjust these sprites according to its own location and size.
    It can also be used to follow a specific game object.
    """
    def __init__(self, location, size, game):
        self.location = location
        self.location.register(self)
        self.size = size
        self.size.register(self)
        self.game = game
        self.batch = pyglet.graphics.Batch()
        self.groups = {
            Layer.background: pyglet.graphics.OrderedGroup(Layer.background),
            Layer.middle: pyglet.graphics.OrderedGroup(Layer.middle),
            Layer.foreground: pyglet.graphics.OrderedGroup(Layer.foreground),
        }
        self.sprites = {}
        self._follow = None

    def follow(self, game_object):
        self._follow = game_object

    def draw(self):
        self.batch.draw()

    def update_for_object(self, game_object):
        sprite = self.sprites.get(game_object)
        image = game_object.display.current
        if sprite is None:
            group = self.groups.get(game_object.display.layer)
            sprite = pyglet.sprite.Sprite(image, batch=self.batch, group=group)
            self.sprites[game_object] = sprite
        else:
            if image != sprite.image:
                sprite.image = image
        self.adjust_game_object_sprite(game_object, sprite)

    def update(self):
        if self._follow:
            cx, cy = self.size.center_rectangle.x, self.size.center_rectangle.y
            fx, fy = self._follow.location.x, self._follow.location.y
            x_dist = fx - cx
            y_dist = fy - cy
            if abs(x_dist) > 32:
                self.location.add(x=util.sign(x_dist))

            if abs(y_dist) > 32:
                self.location.add(y=util.sign(y_dist))


    def adjust_game_object_sprite(self, game_object, sprite):
        """
        Will adjust a game object's sprite based on
        :param game_object: The game object to adjust
        """
        if self.is_visible(game_object):
            sprite.visible = True
            pixel_coordinate = self.coord_to_pixel(game_object.location.x, game_object.location.y)
            sprite.set_position(*pixel_coordinate)
        else:
            sprite.visible = False

    def pixel_to_coord(self, pixel_x, pixel_y):
        return self.location.x + pixel_x, self.location.y + pixel_y

    def coord_to_pixel(self, coord_x, coord_y):
        return coord_x - self.location.x, self.size.height - (coord_y - self.location.y)

    def is_visible(self, game_object):
        if self.size.rectangle.intersects(game_object.size.rectangle):
            return True
        return False
