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
        elif 0 < actor.physics.velocity_x < 1:
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
        elif 0 > actor.physics.velocity_x > -1:
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
            actor.physics.velocity_x -= 0.5
        elif actor.physics.velocity_x > -0.5:
            actor.physics.velocity_x = -0.5
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
            actor.physics.velocity_x += 0.5
        elif 0 < actor.physics.velocity_x < 0.5:
            actor.physics.velocity_x = 0.5
        actor.flipped = False


class Jump(Action):
    def execute(self):
        pass

    def can_execute(self):
        return self.actor.physics.bottom_collisions

    def on_start(self):
        actor = self.actor
        actor.physics.velocity_y -= 16
        actor.physics.velocity_x += actor.physics.velocity_x
        actor.stance.change_stance('jumping')

    @property
    def finished(self):
        return self.actor.physics.bottom_collisions


class ClimbUp(Action):
    continuous = True

    def execute(self):
        self.actor.physics.velocity_y = -1

    def can_execute(self):
        if self.actor.physics.top_climbables or self.actor.physics.center_climbables:
            return True
        return False

    def on_start(self):
        actor = self.actor
        actor.stance.change_stance('climbing')
        actor.display.play('climb')

    def on_stop(self):
        actor = self.actor
        if not self.actor.physics.top_climbables and not self.actor.physics.center_climbables:
            actor.stance.change_stance('idle')

    @property
    def finished(self):
        return not self.actor.physics.top_climbables and not self.actor.physics.center_climbables


class ClimbDown(Action):
    continuous = True

    def execute(self):
        self.actor.physics.velocity_y = 1

    def can_execute(self):
        if any(self.actor.physics.climbables):
            return True
        return False

    def on_start(self):
        actor = self.actor
        actor.stance.change_stance('climbing')
        actor.display.play('climb')
        actor.physics.climbing_down = True

    def on_stop(self):
        actor = self.actor
        actor.physics.climbing_down = False
        self.actor.physics.velocity_y = 0
        if not any(self.actor.physics.climbables) or self.actor.physics.bottom_collisions:
            actor.stance.change_stance('idle')

    @property
    def finished(self):
        return not any(self.actor.physics.climbables) or self.actor.physics.bottom_collisions


class ClimbLeft(Action):
    continuous = True

    def execute(self):
        self.actor.physics.velocity_x = -1

    def can_execute(self):
        if self.actor.physics.center_climbables or self.actor.physics.left_climbables:
            return True
        return False

    def on_start(self):
        actor = self.actor
        actor.stance.change_stance('climbing')
        actor.display.play('climb')

    def on_stop(self):
        actor = self.actor
        if not self.actor.physics.center_climbables and not self.actor.physics.left_climbables:
            actor.stance.change_stance('idle')

    @property
    def finished(self):
        return not self.actor.physics.center_climbables and not self.actor.physics.left_climbables


class ClimbRight(Action):
    continuous = True

    def execute(self):
        self.actor.physics.velocity_x = 1

    def can_execute(self):
        if self.actor.physics.center_climbables or self.actor.physics.right_climbables:
            return True
        return False

    def on_start(self):
        actor = self.actor
        actor.stance.change_stance('climbing')
        actor.display.play('climb')

    def on_stop(self):
        actor = self.actor
        if not actor.physics.center_climbables and not actor.physics.right_climbables:
            actor.stance.change_stance('idle')

    @property
    def finished(self):
        actor = self.actor
        return not actor.physics.center_climbables and not actor.physics.right_climbables
