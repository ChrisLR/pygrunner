from pygrunner.core.components import listing
from pygrunner.core.components.base import Component
from enum import Enum
from pygrunner.core import util


class RestrictKeyword(Enum):
    Any = 0
    Allies = 1
    Enemies = 2


@listing.register
class KillTouch(Component):
    """
    This component will kill objects
    """

    name = "killtouch"

    def __init__(self, damage=99, knockback=None, only_on_fall=False, zone="center"):
        super().__init__()
        self.damage = damage
        self.triggered = False
        self.only_on_fall = only_on_fall
        self.knockback = knockback
        self.zone = zone

    def update(self):
        # TODO Handle restrictions
        host_physics = self.host.physics
        intersects = host_physics.intersects
        if intersects:
            self._trigger(intersects)
        else:
            if self.triggered is True:
                self._relax()

    def trigger(self, game_object, rect_name):
        if self.only_on_fall and not game_object.physics.velocity_y > 1:
            return

        if not rect_name == self.zone:
            return

        if self.knockback:
            if not game_object.health.is_invincible:
                game_object.physics.velocity_y = -16
                game_object.physics.velocity_x = util.sign(
                    game_object.location.x - self.host.location.x) * 4

        game_object.health.damage(self.damage)

        self.triggered = True

    def _trigger(self, intersects):
        for game_object in intersects:
            game_object.health.damage(self.damage)

        self.triggered = True
        self.host.display.play('trigger')

    def _relax(self):
        self.triggered = False
        self.host.display.play('idle')

    def reset(self):
        self.damage = 99
        self.triggered = False

    def register(self, host):
        super().register(host)
        triggerable = getattr(self.host, 'triggers', None)
        if triggerable is not None:
            triggerable.add(self)
