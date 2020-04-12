import pyglet
from pyglet import gl

from pygrunner.core import util
from pygrunner.core.layers import Layer
from pyglet.window import FPSDisplay


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
        self.display = None
        self._initialize_opengl()
        self.physics = None
        self._fps_display = FPSDisplay(self.game.window)

    def _initialize_opengl(self):
        # Initialize Projection matrix
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        # Initialize Modelview matrix
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        # Set alpha blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glViewport(0, 0, self.size.width, self.size.height)

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
        rectangle = self.size.rectangle
        gl.glPushMatrix()
        gl.glScalef(1, -1, 0)
        gl.glOrtho(rectangle.left, rectangle.right, rectangle.bottom, rectangle.top, -1, 1)
        self.batch.draw()
        gl.glPopMatrix()
        gl.glPushMatrix()
        gl.glOrtho(0, rectangle.width, 0, rectangle.height, -1, 1)
        self.ui_batch.draw()
        gl.glPopMatrix()
        self._fps_display.draw()

    def follow(self, game_object):
        self._follow = game_object
        # TODO Additional work required for level transitions here
        self.adjust_background_image()

    def update(self):
        self.hud.update()
        if self._follow:
            follow_location = self._follow.location
            center_rectangle = self.size.center_rectangle
            cx, cy = center_rectangle.x, center_rectangle.y
            fx, fy = follow_location.x, follow_location.level.height - follow_location.y
            x_dist = fx - cx
            y_dist = fy - cy

            x_spd = 0
            y_spd = 0
            if abs(x_dist) > 30:
                speed_multiplier = round(x_dist / 32)
                sign = util.sign(x_dist)
                speed = sign if -1 < speed_multiplier < 1 else speed_multiplier
                x_spd = speed

            if abs(y_dist) > 30:
                speed_multiplier = round(y_dist / 32)
                sign = util.sign(y_dist)
                speed = sign if -1 < speed_multiplier < 1 else speed_multiplier
                y_spd = speed

            self.location.add(x=x_spd, y=y_spd)

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
