from pygrunner.core import geom
from pygrunner.core.components.base import Component


class Location(Component):
    name = "location"

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

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
            self.host.size.adjust_rectangles()


    def set(self, x=None, y=None):
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        self.host.size.adjust_rectangles()

    def reset(self):
        self.x = 0
        self.y = 0