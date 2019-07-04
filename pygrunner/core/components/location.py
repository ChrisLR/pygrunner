from pygrunner.core import geom
from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class Location(Component):
    name = "location"

    def __init__(self, x, y, level=None):
        super().__init__()
        self.x = x
        self.y = y
        self.level = level

    @property
    def point(self):
        return geom.Point(self.x, self.y)

    @property
    def tuple(self):
        return self.x, self.y

    def add(self, x=0, y=0):
        if x != 0 or y != 0:
            self.x += x
            self.y += y
            host = self.host
            host.size.adjust_rectangles()
            if host.display is not None:
                host.display.location_changed = True

    def set(self, x=None, y=None):
        if x is None and y is None:
            return

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        self.host.size.adjust_rectangles()
        self.host.display.location_changed = True

    def reset(self):
        self.x = 0
        self.y = 0
