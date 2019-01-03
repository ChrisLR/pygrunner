from pygrunner.core import geom
from pygrunner.core.components.base import Component


class Size(Component):
    def __init__(self, height=16, width=16):
        super().__init__()
        self.height = height
        self.width = width
        self.rectangle = geom.Rectangle(0, 0, width, height)
        self.bottom_rectangle = geom.Rectangle(0, height, width, 1)
        self.top_rectangle = geom.Rectangle(0, 0, width, 1)
        self.right_rectangle = geom.Rectangle(width, 0, 1, height)
        self.left_rectangle = geom.Rectangle(0, 0, 1, height)

    
    def update(self):
        x, y = self.host.location.tuple
        self.rectangle.x = x
        self.rectangle.y = y
        self.bottom_rectangle.x = x
        self.bottom_rectangle.y = y + self.height
        self.top_rectangle.x = x
        self.top_rectangle.y = y
        self.left_rectangle.x = x
        self.left_rectangle.y = y
        self.right_rectangle.x = x + self.width
        self.right_rectangle.y = y