from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class Collector(Component):
    name = "collector"

    def __init__(self, include_types=None):
        super().__init__()
        self.collected_values = {}
        self.include_types = include_types

    def update(self):
        host_physics = self.host.physics
        if host_physics and host_physics.collisions:
            for collision in host_physics.intersects:
                collectible = collision.collectible
                if collectible and self._can_collect(collectible):
                    self._collect(collision, collectible)


    def _can_collect(self, collectible):
        return self.include_types is None or collectible.collectible_type in self.include_types

    def _collect(self, game_object, collectible):
        game_object.recycle = True
        current_value = self.collected_values.setdefault(collectible.collectible_type, 0)
        self.collected_values[collectible.collectible_type] = current_value + collectible.value

    def reset(self):
        self.collected_values.clear()
