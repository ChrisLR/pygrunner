from pygrunner.core import geom
from pygrunner.core.components.base import Component


class Size(Component):
    name = "size"

    def __init__(self, height=16, width=16):
        super().__init__()
        self.height = height
        self.width = width
        self.center_x = int(round(width / 2))
        self.center_y = int(round(height / 2))
        self.rectangle = geom.Rectangle(0, 0, width, height)
        self.bottom_rectangle = geom.Rectangle(1, height, width - 2, 1)
        self.top_rectangle = geom.Rectangle(1, 0, width - 2, 1)
        self.right_rectangle = geom.Rectangle(width, 0, 1, height)
        self.left_rectangle = geom.Rectangle(0, 0, 1, height)
        self.center_rectangle = geom.Rectangle(self.center_x, self.center_y,
                                               int(round(width / 4)), int(round(height / 4)))

    def adjust_rectangles(self):
        if self.host:
            new_x, new_y = self.host.location.tuple
        else:
            new_x, new_y = 0, 0

        self.rectangle.x = new_x
        self.rectangle.y = new_y
        self.bottom_rectangle.x = new_x + 1
        self.bottom_rectangle.y = new_y + self.height
        self.top_rectangle.x = new_x + 1
        self.top_rectangle.y = new_y
        self.left_rectangle.x = new_x
        self.left_rectangle.y = new_y
        self.right_rectangle.x = new_x + self.width
        self.right_rectangle.y = new_y
        self.center_rectangle.x = new_x + self.center_x
        self.center_rectangle.y = new_y + self.center_y

    def update(self):
        pass


    def reset(self):
        self.height = 0
        self.width = 0
        self.center_x = 0
        self.center_y = 0
        self.rectangle.x = 0
        self.rectangle.y = 0
        self.bottom_rectangle.x = 0
        self.bottom_rectangle.y = 0
        self.top_rectangle.x = 0
        self.top_rectangle.y = 0
        self.left_rectangle.x = 0
        self.left_rectangle.y = 0
        self.right_rectangle.x = 0
        self.right_rectangle.y = 0
        self.center_rectangle.x = 0
        self.center_rectangle.y = 0
