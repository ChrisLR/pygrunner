from enum import Enum


class Layer(Enum):
    image_background = 0
    background = 1
    middle = 2
    foreground = 3

    def __lt__(self, other):
        return self.value < other.value
