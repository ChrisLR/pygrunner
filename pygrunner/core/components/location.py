from pygrunner.core import geom
from pygrunner.core.components.base import Component


class Location(Component):
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
