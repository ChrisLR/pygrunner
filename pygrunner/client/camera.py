import pyglet
from pyglet.gl import *

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
        self.ui_batch = pyglet.graphics.Batch()
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
        self.hud.assign(self.ui_batch, self.groups[Layer.foreground])
        # Initialize Projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Initialize Modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Set antialiasing
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        # Set alpha blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glViewport(0, 0, self.size.width, self.size.height)

    def adjust_background_image(self):
        if self.location and self.location.level:
            current_level = self.location.level
            if current_level.background_image != self._background_image:
                ox, oy = current_level.background_image_offset
                group = self.groups[Layer.image_background]
                sprite = pyglet.sprite.Sprite(
                    current_level.background_image, x=ox, y=oy, batch=self.batch, group=group)
                # TODO Not sure DEL is appropriate here
                del self._background_sprite
                self._background_sprite = sprite
            elif current_level.background_image_offset != self._background_image_offset:
                ox, oy = current_level.background_image_offset
                self._background_sprite.x = ox
                self._background_sprite.y = oy

    def draw(self):
        # Save the default modelview matrix
        glPushMatrix()

        # Set orthographic projection matrix
        rectangle = self.size.rectangle
        glScalef(1, -1, 0)
        glOrtho(rectangle.left, rectangle.right, rectangle.bottom, rectangle.top, -1, 1)

        # Draw
        self.batch.draw()

        # Remove default modelview matrix
        glPopMatrix()
        glPushMatrix()
        glOrtho(0, rectangle.width, 0, rectangle.height, -1, 1)
        self.ui_batch.draw()
        glPopMatrix()

    def follow(self, game_object):
        self._follow = game_object
        # TODO Additional work required for level transitions here
        self.adjust_background_image()

    def update(self):
        self.hud.update()
        if self._follow:
            cx, cy = self.size.center_rectangle.x, self.size.center_rectangle.y
            fx, fy = self._follow.location.x, self.location.level.height - self._follow.location.y
            x_dist = fx - cx
            y_dist = fy - cy

            if abs(x_dist) > 30:
                speed_multiplier = round(x_dist / 32)
                sign = util.sign(x_dist)
                speed = sign if -1 < speed_multiplier < 1 else speed_multiplier
                self.location.add(x=speed)

            if abs(y_dist) > 30:
                speed_multiplier = round(y_dist / 32)
                sign = util.sign(y_dist)
                speed = sign if -1 < speed_multiplier < 1 else speed_multiplier
                self.location.add(y=speed)

    def update_for_object(self, game_object):
        object_display = game_object.display
        sprite = object_display.sprite
        if sprite and game_object.recycle:
            sprite.visible = False
            object_display.sprite = None
            return

        image = object_display.current
        if sprite is None:
            group = self.groups.get(object_display.layer)
            sprite = pyglet.sprite.Sprite(image, batch=self.batch, group=group)
            object_display.sprite = sprite
        else:
            if image is not None and image != sprite.image:
                sprite.image = image

    def coord_to_pixel(self, coord_x, coord_y):
        return coord_x - self.location.x, self.size.height - (coord_y - self.location.y)

    def pixel_to_coord(self, pixel_x, pixel_y):
        return self.location.x + pixel_x, self.location.y + pixel_y
