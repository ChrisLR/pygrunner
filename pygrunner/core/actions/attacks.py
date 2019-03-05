from pygrunner.core import util
from pygrunner.core.actions.base import Action


class Punch(Action):
    cancelable = False
    continuous = False

    def __init__(self, actor):
        super().__init__(actor)
        self.updates = 0

    def can_execute(self):
        return True

    def execute(self):
        self.updates += 1
        # TODO This must take factions into account
        targets = [character for character in self.actor.physics.intersects]
        for target in targets:
            target_health = target.health
            if target_health and not target_health.is_dead:
                # TODO Damage will vary
                target_health.damage(1)

            if not target_health.is_dead:
                # TODO Knockback force must vary
                target.physics.velocity_y = -4
                target.physics.velocity_x = util.sign(target.location.x - self.actor.location.x) * 4

    def on_start(self):
        actor = self.actor
        actor.display.play('punch')
        actor.stance.change_stance('punching')

    def on_stop(self):
        self.updates = 0
        self.actor.display.play('idle')

    @property
    def finished(self):
        # TODO We must have a way to find if the animation has ended.
        return self.updates >= 20
