from pygrunner.core.components import listing
from pygrunner.core.components.base import Component
from enum import Enum


class RestrictKeyword(Enum):
    Any = 0
    Allies = 1
    Enemies = 2


@listing.register
class Bouncer(Component):
    """
    This component will bounce objects
    """

    name = "bouncer"

    def __init__(self, vertical_force=0, horizontal_force=0, restrict=RestrictKeyword.Any):
        super().__init__()
        self.vertical_force = vertical_force
        self.horizontal_force = horizontal_force
        self.restrict = restrict
        self.triggered = False

    def update(self):
        # TODO Handle restrictions
        host_physics = self.host.physics
        intersects = host_physics.intersects
        if intersects:
            if self.triggered is False:
                self._trigger(intersects)
        else:
            if self.triggered is True:
                self._relax()

    def _trigger(self, intersects):
        has_triggered = False
        for game_object in intersects:
            if self.vertical_force:
                has_triggered = True
                game_object.physics.velocity_y = self.vertical_force

            if self.horizontal_force:
                has_triggered = True
                game_object.physics.velocity_x = self.horizontal_force

        if has_triggered is True:
            self.triggered = True
            self.host.display.play('bounce')

    def _relax(self):
        self.triggered = False
        self.host.display.play('idle')

    def reset(self):
        self.vertical_force = 0
        self.horizontal_force = 0
        self.restrict = RestrictKeyword.Any
        self.triggered = False
