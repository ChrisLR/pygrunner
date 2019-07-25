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
        facing_left = self.actor.flipped
        actor_rectangle = self.actor.size.center_rectangle
        targets = [character for character in self.actor.physics.intersects]
        for target in targets:
            if facing_left:
                if target.size.center_rectangle.left >= actor_rectangle.right:
                    continue
            else:
                if target.size.center_rectangle.right <= actor_rectangle.left:
                    continue
            target_health = target.health
            if target_health is None:
                continue

            target_invincible = target_health.is_invincible if target_health else False
            target_is_dead = target_health.is_dead if target_health else False
            if target_health and not target_is_dead:
                # TODO Damage will vary
                target_health.damage(1)

            if not target_is_dead and not target_invincible:
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


class Swoop(Action):
    cancelable = False
    continuous = False

    def __init__(self, actor):
        super().__init__(actor)
        self.updates = 0

    def can_execute(self):
        return True

    def execute(self):
        # TODO This has copypasta, remedy this
        self.updates += 1
        # TODO This must take factions into account
        facing_left = self.actor.flipped
        actor_rectangle = self.actor.size.center_rectangle
        targets = [character for character in self.actor.physics.intersects]
        for target in targets:
            if facing_left:
                if target.size.center_rectangle.left >= actor_rectangle.right:
                    continue
            else:
                if target.size.center_rectangle.right <= actor_rectangle.left:
                    continue
            target_health = target.health
            if target_health is None:
                continue
            target_invincible = target_health.is_invincible if target_health else False
            target_is_dead = target_health.is_dead if target_health else False
            if target_health and not target_is_dead:
                # TODO Damage will vary
                target_health.damage(1)

            if not target_is_dead and not target_invincible:
                # TODO Knockback force must vary
                target.physics.velocity_y = -4
                target.physics.velocity_x = util.sign(target.location.x - self.actor.location.x) * 4

    def on_start(self):
        actor = self.actor
        actor.display.play('punch')
        actor.stance.change_stance('punching')
        sign = util.sign(actor.physics.velocity_x)
        actor.physics.velocity_x = actor.recipe.move_speed * 10 * sign

    def on_stop(self):
        self.updates = 0
        self.actor.display.play('idle')
        self.actor.physics.velocity_x /= 2

    @property
    def finished(self):
        # TODO We must have a way to find if the animation has ended.
        return self.updates >= 20
