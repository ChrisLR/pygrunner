import pyglet

from pygrunner.core import util
from pygrunner.core.layers import Layer


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
            Layer.image_background: pyglet.graphics.OrderedGroup(Layer.image_background),
            Layer.background: pyglet.graphics.OrderedGroup(Layer.background),
            Layer.middle: pyglet.graphics.OrderedGroup(Layer.middle),
            Layer.foreground: pyglet.graphics.OrderedGroup(Layer.foreground),
        }
        self._follow = None
        self._background_image = None
        self._background_image_offset = None
        self._background_sprite = None
        self.adjust_background_image()
        self.hud = game.hud
        self.hud.assign(self.batch, self.groups[Layer.foreground])

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

    def adjust_background_image(self):
        if self.location and self.location.level:
            current_level = self.location.level
            if current_level.background_image != self._background_image:
                ox, oy = current_level.background_image_offset
                group = self.groups[Layer.image_background]
                sprite = pyglet.sprite.Sprite(
                    current_level.background_image,
                    x=ox, y=oy, batch=self.batch, group=group)
                # TODO Not sure DEL is appropriate here
                del self._background_sprite
                self._background_sprite = sprite
            elif current_level.background_image_offset != self._background_image_offset:
                ox, oy = current_level.background_image_offset
                self._background_sprite.x = ox
                self._background_sprite.y = oy

    def draw(self):
        self.batch.draw()

    def follow(self, game_object):
        self._follow = game_object
        # TODO Additional work required for level transitions here
        self.adjust_background_image()

    def update(self):
        self.hud.update()
        if self._follow:
            cx, cy = self.size.center_rectangle.x, self.size.center_rectangle.y
            fx, fy = self._follow.location.x, self._follow.location.y
            x_dist = fx - cx
            y_dist = fy - cy

            if abs(x_dist) > 30:
                speed_multiplier = round(x_dist / 16)
                sign = util.sign(x_dist)
                speed = sign if speed_multiplier < 1 else speed_multiplier
                self.location.add(x=speed)

            if abs(y_dist) > 30:
                speed_multiplier = round(y_dist / 16)
                sign = util.sign(y_dist)
                speed = sign if speed_multiplier < 1 else speed_multiplier
                self.location.add(y=speed)

    def update_for_object(self, game_object):
        object_display = game_object.display
        sprite = object_display.sprite
        if sprite and game_object.recycle:
            sprite.visible = False
            game_object.display.sprite = None
            return

        image = game_object.display.current
        if sprite is None:
            group = self.groups.get(game_object.display.layer)
            sprite = pyglet.sprite.Sprite(image, batch=self.batch, group=group)
            object_display.sprite = sprite
        else:
            if image != sprite.image:
                sprite.image = image
        self.adjust_game_object_sprite(game_object, sprite)

    def coord_to_pixel(self, coord_x, coord_y):
        return coord_x - self.location.x, self.size.height - (coord_y - self.location.y)

    def pixel_to_coord(self, pixel_x, pixel_y):
        return self.location.x + pixel_x, self.location.y + pixel_y

    def is_visible(self, game_object):
        if self.size.rectangle.intersects(game_object.size.rectangle):
            return True
        return False
