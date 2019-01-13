from enum import Enum


class Layer(Enum):
    background = 0
    middle = 1
    foreground = 2

    def __lt__(self, other):
        return self.value < other.value
