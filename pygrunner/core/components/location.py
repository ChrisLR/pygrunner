from pygrunner.core import geom
from pygrunner.core.components import listing
from pygrunner.core.components.base import Component
import math


@listing.register
class Location(Component):
    name = "location"

    def __init__(self, x, y, level=None):
        super().__init__()
        self.x = x
        self.y = y
        self.level = level
        self.grid_x = int(x / 32)
        self.grid_y = int(x / 32)

    @property
    def grid_point(self):
        return geom.Point(self.grid_x, self.grid_y)

    @property
    def point(self):
        return geom.Point(self.x, self.y)

    @property
    def tuple(self):
        return self.x, self.y

    def add(self, x=0, y=0):
        if x != 0:
            self.x += x
            self.grid_x = round(self.x / 32)
            # if x > 0:
            #     self.grid_x = math.floor(self.x / 32)
            # elif x < 0:
            #     self.grid_x = math.ceil(self.x / 32)

        if y != 0:
            self.y += y
            self.grid_y = round(self.y / 32)
            # if y > 0:
            #     self.grid_y = math.floor(self.y / 32)
            # elif y < 0:
            #     self.grid_y = math.ceil(self.y / 32)

        if x != 0 or y != 0:
            host = self.host
            host.size.adjust_rectangles()
            if host.display is not None:
                host.display.location_changed = True

    def set(self, x=None, y=None):
        if x is None and y is None:
            return

        if x is not None:
            self.x = x
            self.grid_x = int(x / 32)

        if y is not None:
            self.y = y
            self.grid_y = int(y / 32)

        self.host.size.adjust_rectangles()
        self.host.display.location_changed = True

    def reset(self):
        self.x = 0
        self.y = 0
        self.grid_x = 0
        self.grid_y = 0

