from pygrunner.core import geom
from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class Size(Component):
    name = "size"

    def __init__(self, height=32, width=32):
        super().__init__()
        self.height = height
        self.width = width
        self.half_width = int(round(width / 2))
        self.half_height = int(round(height / 2))
        self.rectangle = geom.Rectangle(0, 0, width, height)
        self.center_rectangle = geom.Rectangle(
            self.half_width, self.half_height,
            int(round(width / 4)), int(round(height / 4)))

    def adjust_rectangles(self):
        if self.host:
            new_x, new_y = self.host.location.tuple
        else:
            new_x, new_y = 0, 0

        self.rectangle.x = new_x
        self.rectangle.y = new_y
        self.center_rectangle.x = new_x + self.half_width
        self.center_rectangle.y = new_y + self.half_height

    def update(self):
        pass

    def reset(self):
        self.height = 0
        self.width = 0
        self.half_width = 0
        self.half_height = 0
        self.rectangle.x = 0
        self.rectangle.y = 0
        self.center_rectangle.x = 0
        self.center_rectangle.y = 0
