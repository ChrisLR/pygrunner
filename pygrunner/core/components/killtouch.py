from pygrunner.core.components import listing
from pygrunner.core.components.base import Component
from enum import Enum


class RestrictKeyword(Enum):
    Any = 0
    Allies = 1
    Enemies = 2


@listing.register
class KillTouch(Component):
    """
    This component will bounce objects
    """

    name = "bouncer"

    def __init__(self, damage=99):
        super().__init__()
        self.damage = damage
        self.triggered = False

    def update(self):
        # TODO Handle restrictions
        host_physics = self.host.physics
        intersects = host_physics.intersects
        if intersects:
            self._trigger(intersects)
        else:
            if self.triggered is True:
                self._relax()

    def _trigger(self, intersects):
        has_triggered = False
        for game_object in intersects:
            game_object.health.damage(self.damage)

        if has_triggered is True:
            self.triggered = True
            self.host.display.play('trigger')

    def _relax(self):
        self.triggered = False
        self.host.display.play('idle')

    def reset(self):
        self.damage = 99
        self.triggered = False
