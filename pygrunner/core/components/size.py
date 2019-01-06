from pygrunner.core import geom
from pygrunner.core.components.base import Component


class Size(Component):
    name = "size"

    def __init__(self, height=16, width=16):
        super().__init__()
        self.height = height
        self.width = width
        self.rectangle = geom.Rectangle(0, 0, width, height)
        self.bottom_rectangle = geom.Rectangle(0, height, width, 1)
        self.top_rectangle = geom.Rectangle(0, 0, width, 1)
        self.right_rectangle = geom.Rectangle(width, 0, 1, height)
        self.left_rectangle = geom.Rectangle(0, 0, 1, height)

    def adjust_rectangles(self):
        if self.host:
            new_x, new_y = self.host.location.tuple
        else:
            new_x, new_y = 0, 0

        self.rectangle.x = new_x
        self.rectangle.y = new_y
        self.bottom_rectangle.x = new_x
        self.bottom_rectangle.y = new_y + self.height
        self.top_rectangle.x = new_x
        self.top_rectangle.y = new_y
        self.left_rectangle.x = new_x
        self.left_rectangle.y = new_y
        self.right_rectangle.x = new_x + self.width
        self.right_rectangle.y = new_y

    def update(self):
        pass


    def reset(self):
        self.height = 0
        self.width = 0
        self.rectangle.x = 0
        self.rectangle.y = 0
        self.bottom_rectangle.x = 0
        self.bottom_rectangle.y = 0 + self.height
        self.top_rectangle.x = 0
        self.top_rectangle.y = 0
        self.left_rectangle.x = 0
        self.left_rectangle.y = 0
        self.right_rectangle.x = 0 + self.width
        self.right_rectangle.y = 0