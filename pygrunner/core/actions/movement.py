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
        move_speed = actor.recipe.move_speed
        if actor.physics.velocity_x <= 0:
            actor.physics.velocity_x += move_speed
        elif 0 < actor.physics.velocity_x < move_speed:
            actor.physics.velocity_x = move_speed
        actor.flipped = False

    def on_start(self):
        actor = self.actor
        actor.display.play('run')
        actor.stance.change_stance('running')


class WalkLeft(Action):
    continuous = True

    def execute(self):
        actor = self.actor
        move_speed = actor.recipe.move_speed
        if actor.physics.velocity_x >= 0:
            actor.physics.velocity_x -= move_speed
        elif 0 > actor.physics.velocity_x > -move_speed:
            actor.physics.velocity_x = -move_speed
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
        half_speed = actor.recipe.move_speed / 2
        if actor.physics.velocity_x >= 0:
            actor.physics.velocity_x -= half_speed
        elif actor.physics.velocity_x > -half_speed:
            actor.physics.velocity_x = -half_speed
        actor.flipped = True

    def can_execute(self):
        return True


class GlideRight(Action):
    continuous = True

    def can_execute(self):
        return True

    def execute(self):
        actor = self.actor
        half_speed = actor.recipe.move_speed / 2
        if actor.physics.velocity_x <= 0:
            actor.physics.velocity_x += half_speed
        elif 0 < actor.physics.velocity_x < half_speed:
            actor.physics.velocity_x = half_speed
        actor.flipped = False


class Jump(Action):
    def execute(self):
        pass

    def can_execute(self):
        return self.actor.physics.bottom_collisions

    def on_start(self):
        actor = self.actor
        actor.physics.velocity_y -= actor.recipe.jump_height
        actor.physics.velocity_x += actor.physics.velocity_x
        actor.stance.change_stance('jumping')

    @property
    def finished(self):
        return self.actor.physics.bottom_collisions


class ClimbUp(Action):
    continuous = True

    def execute(self):
        actor = self.actor
        actor.physics.velocity_y = -actor.recipe.move_speed

    def can_execute(self):
        if any(self.actor.physics.climbables.values()):
            return True
        return False

    def on_start(self):
        actor = self.actor
        actor.stance.change_stance('climbing')
        actor.display.play('climb')
        actor.physics.affected_by_gravity = False

    def on_stop(self):
        actor = self.actor
        self.actor.physics.velocity_y = 0
        if not any(self.actor.physics.climbables.values()):
            actor.stance.change_stance('idle')
            actor.physics.affected_by_gravity = True

    @property
    def finished(self):
        return not any(self.actor.physics.climbables.values())


class ClimbDown(Action):
    continuous = True

    def execute(self):
        actor = self.actor
        self.actor.physics.velocity_y = actor.recipe.move_speed

    def can_execute(self):
        if any(self.actor.physics.climbables.values()):
            return True
        return False

    def on_start(self):
        actor = self.actor
        actor.stance.change_stance('climbing')
        actor.display.play('climb')
        actor.physics.climbing_down = True
        actor.physics.affected_by_gravity = False

    def on_stop(self):
        actor = self.actor
        actor.physics.climbing_down = False
        self.actor.physics.velocity_y = 0
        if not any(self.actor.physics.climbables.values()) or self.actor.physics.bottom_collisions:
            actor.stance.change_stance('idle')
            actor.physics.affected_by_gravity = True

    @property
    def finished(self):
        return not any(self.actor.physics.climbables.values()) or self.actor.physics.bottom_collisions


class ClimbLeft(Action):
    continuous = True

    def execute(self):
        actor = self.actor
        actor.physics.velocity_x = -actor.recipe.move_speed

    def can_execute(self):
        if any(self.actor.physics.climbables.values()):
            return True
        return False

    def on_start(self):
        actor = self.actor
        actor.stance.change_stance('climbing')
        actor.display.play('climb')
        actor.physics.affected_by_gravity = False

    def on_stop(self):
        actor = self.actor
        if not any(self.actor.physics.climbables.values()):
            actor.stance.change_stance('idle')
            actor.physics.affected_by_gravity = True

    @property
    def finished(self):
        return not any(self.actor.physics.climbables.values())


class ClimbRight(Action):
    continuous = True

    def execute(self):
        actor = self.actor
        self.actor.physics.velocity_x = actor.recipe.move_speed

    def can_execute(self):
        if any(self.actor.physics.climbables.values()):
            return True
        return False

    def on_start(self):
        actor = self.actor
        actor.stance.change_stance('climbing')
        actor.display.play('climb')
        actor.physics.affected_by_gravity = False

    def on_stop(self):
        actor = self.actor
        if not any(self.actor.physics.climbables.values()):
            actor.stance.change_stance('idle')
            actor.physics.affected_by_gravity = True

    @property
    def finished(self):
        return not any(self.actor.physics.climbables.values())
