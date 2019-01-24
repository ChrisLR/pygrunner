from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class Collectible(Component):
    name = "collectible"

    def __init__(self, collectible_type, value):
        super().__init__()
        self.collectible_type = collectible_type
        self.value = value

    def reset(self):
        pass