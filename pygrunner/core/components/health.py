from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class Health(Component):
    name = "health"

    def reset(self):
        self.max = 0
        self.current = 0
        self.is_dead = False

    def __init__(self, max_health):
        super().__init__()
        self.max = max_health
        self.current = max_health
        self.is_dead = False

    def damage(self, amount):
        self.current -= amount
        if self.current <= 0:
            self.is_dead = True
            self.on_death()

    def heal(self, amount):
        if not self.is_dead:
            self.current += amount
            if self.current > self.max:
                self.current = self.max

    def revive(self, health=None):
        self.is_dead = False
        if health is not None:
            self.current = 0
            self.heal(health)
        else:
            self.current = 1
        self.on_revive()

    def on_death(self):
        # TODO Handle being killed
        self.host.display.play("dead")
        pass

    def on_revive(self):
        pass
