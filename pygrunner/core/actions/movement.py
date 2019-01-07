from pygrunner.core.actions.base import Action


class WalkRight(Action):
    def can_execute(self):
        return True

    def execute(self):
        actor = self.actor
        if actor.physics.velocity_x <= 0:
            actor.physics.velocity_x += 1
        else:
            actor.physics.velocity_x = 1
        actor.flipped = False
        actor.display.play('run')


class WalkLeft(Action):
    def execute(self):
        actor = self.actor
        if actor.physics.velocity_x >= 0:
            actor.physics.velocity_x -= 1
        else:
            actor.physics.velocity_x = -1
        actor.flipped = True
        actor.display.play('run')

    def can_execute(self):
        return True


class GlideLeft(Action):
    def execute(self):
        actor = self.actor
        if actor.physics.velocity_x >= 0:
            actor.physics.velocity_x -= 0.5
        else:
            actor.physics.velocity_x = -0.5
        actor.flipped = True

    def can_execute(self):
        return True


class GlideRight(Action):
    def can_execute(self):
        return True

    def execute(self):
        actor = self.actor
        if actor.physics.velocity_x <= 0:
            actor.physics.velocity_x += 0.5
        else:
            actor.physics.velocity_x = 0.5
        actor.flipped = False


class Jump(Action):
    def execute(self):
        actor = self.actor
        if actor.physics.velocity_y == 0:
            actor.physics.velocity_y -= 16

    def can_execute(self):
        return self.actor.physics.bottom_collisions
