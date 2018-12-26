from dataclasses import dataclass
import math


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
        delta_x = abs(self.x - rectangle.x)
        delta_y = abs(self.y - rectangle.y)
        if delta_x > self.width + rectangle.width:
            return False
        if delta_y > self.height + rectangle.height:
            return False

        horizontal = self.right >= rectangle.left and self.left <= rectangle.right
        if horizontal is False:
            horizontal = rectangle.right >= self.left and rectangle.left <= self.right

        if horizontal is False:
            return False

        vertical = self.bottom >= rectangle.top and self.top <= rectangle.bottom
        if vertical is False:
            vertical = rectangle.bottom >= self.top and rectangle.top <= self.bottom

        if vertical is False:
            return False

        return True


@dataclass(eq=True)
class Point:
    x: int
    y: int

    def distance_to(self, point):
        return round(math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2))
