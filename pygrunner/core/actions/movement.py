from pygrunner.core.actions.base import Action


class Idle(Action):
    def can_execute(self):
        return True

    def execute(self):
        pass

    def on_start(self):
        actor = self.actor
        actor.display.play('idle')
        actor.stance.change_stance('idle')

    def on_stop(self):
        pass

class WalkRight(Action):
    continuous = True

    def can_execute(self):
        return True

    def execute(self):
        actor = self.actor
        if actor.physics.velocity_x <= 0:
            actor.physics.velocity_x += 1
        else:
            actor.physics.velocity_x = 1
        actor.flipped = False

    def on_start(self):
        actor = self.actor
        actor.display.play('run')
        actor.stance.change_stance('running')


class WalkLeft(Action):
    continuous = True

    def execute(self):
        actor = self.actor
        if actor.physics.velocity_x >= 0:
            actor.physics.velocity_x -= 1
        else:
            actor.physics.velocity_x = -1
        actor.flipped = True

    def can_execute(self):
        return True

    def on_start(self):
        actor = self.actor
        actor.display.play('run')
        actor.stance.change_stance('running')


class GlideLeft(Action):
    continuous = True

    def execute(self):
        actor = self.actor
        if actor.physics.velocity_x >= 0:
            actor.physics.velocity_x -= 0.1
        else:
            actor.physics.velocity_x = -0.1
        actor.flipped = True

    def can_execute(self):
        return True


class GlideRight(Action):
    continuous = True

    def can_execute(self):
        return True

    def execute(self):
        actor = self.actor
        if actor.physics.velocity_x <= 0:
            actor.physics.velocity_x += 0.1
        else:
            actor.physics.velocity_x = 0.1
        actor.flipped = False


class Jump(Action):
    def execute(self):
        pass

    def can_execute(self):
        return self.actor.physics.bottom_collisions

    def on_start(self):
        actor = self.actor
        if actor.physics.velocity_y == 0:
            actor.physics.velocity_y -= 16
            actor.stance.change_stance('jumping')

    def finished(self):
        return self.actor.physics.bottom_collisions
