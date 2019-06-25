from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class Health(Component):
    name = "health"

    def __init__(self, max_health):
        super().__init__()
        self.max = max_health
        self.current = max_health
        self.is_dead = False
        self.invincible_timer = 0
        self.revive_timer = -1  # 100

    def damage(self, amount):
        if self.invincible_timer:
            return

        self.current -= amount
        self.invincible_timer = 50
        if self.current <= 0:
            self.is_dead = True
            self.on_death()

    def heal(self, amount):
        if not self.is_dead:
            self.current += amount
            if self.current > self.max:
                self.current = self.max

    @property
    def is_invincible(self):
        return self.invincible_timer > 0

    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.revive_timer > 0:
            self.revive_timer -= 1
        elif self.revive_timer == 0:
            self.revive(4)
            self.revive_timer = -1

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
        self.revive_timer = 100

    def on_revive(self):
        self.host.display.play("idle")

    def reset(self):
        self.max = 0
        self.current = 0
        self.is_dead = False
