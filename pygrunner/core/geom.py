from dataclasses import dataclass
import math
from pygrunner.core import util


class Rectangle(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    def intersects(self, rectangle):
        """
        Determines if a rectangle intersects another.
        :type rectangle: Rectangle
        :rtype bool
        """

        return self.right >= rectangle.left and self.left <= rectangle.right and self.bottom >= rectangle.top and self.top <= rectangle.bottom


@dataclass(eq=True)
class Point:
    x: int
    y: int

    def distance_to(self, point):
        return round(math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2))

    def direction_to(self, point):
        dx = util.sign(point.x - self.x)
        dy = util.sign(point.y - self.y)

        return Point(dx, dy)

    def point_distance_to(self, point):
        return Point(round(math.sqrt((self.x - point.x) ** 2)), round(math.sqrt((self.y - point.y) ** 2)))
