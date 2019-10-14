from pygrunner.core import actions
from pygrunner.core.keymap import Keymap


class Stance(object):
    """
    Represents both the state of an object and the actions available to it
    """
    name = ""

    def __init__(self, actor):
        self.actor = actor
        self.executing_action = None

    def do_keymaps(self, keymaps):
        pass

    def start_or_continue(self, action_type):
        health = self.actor.health
        if health and health.is_dead:
            if self.executing_action:
                self.executing_action.on_stop()
                self.executing_action = None
            self.actor.stance.change_stance('dead')
            return

        current_action_type = type(self.executing_action)
        if current_action_type is action_type:
            return self.continue_current_action()

        if self.executing_action is not None:
            if not self.executing_action.finished and not self.executing_action.cancelable:
                return self.continue_current_action()
            else:
                self.executing_action.on_stop()
                self.executing_action = None

        new_action = action_type(self.actor)
        if new_action.can_execute():
            self.executing_action = new_action
            new_action.on_start()
            new_action.execute()

    def continue_current_action(self, stop_continuous=False):
        health = self.actor.health
        if health and health.is_dead:
            self.actor.stance.change_stance('dead')
            return

        if self.executing_action is None:
            return

        if self.executing_action.can_execute():
            self.executing_action.execute()
            if self.executing_action.finished or (stop_continuous and self.executing_action.continuous):
                self.executing_action.on_stop()
                self.executing_action = None
        else:
            self.executing_action.on_stop()
            self.executing_action = None


class Idle(Stance):
    name = "idle"

    def do_keymaps(self, keymaps):
        if not keymaps:
            if self.executing_action:
                self.continue_current_action(stop_continuous=True)
            else:
                self.start_or_continue(actions.Idle)

        if Keymap.A in keymaps:
            # TODO Stances will have to vary from actor to actor
            self.start_or_continue(actions.Punch)

        if Keymap.Left in keymaps:
            self.start_or_continue(actions.WalkLeft)
        elif Keymap.Right in keymaps:
            self.start_or_continue(actions.WalkRight)

        if Keymap.B in keymaps:
            self.start_or_continue(actions.Jump)

        if Keymap.Up in keymaps:
            self.start_or_continue(actions.ClimbUp)
        elif Keymap.Down in keymaps:
            self.start_or_continue(actions.ClimbDown)


class Running(Idle):
    name = "running"


class Jumping(Stance):
    name = "jumping"

    def do_keymaps(self, keymaps):
        if Keymap.Left in keymaps:
            self.start_or_continue(actions.GlideLeft)
        elif Keymap.Right in keymaps:
            self.start_or_continue(actions.GlideRight)

        if not keymaps and self.executing_action:
            self.continue_current_action(stop_continuous=True)

        if self.actor.physics.velocity_y >= 0 and self.actor.physics.bottom_collisions:
            self.start_or_continue(actions.Idle)


class Climbing(Stance):
    name = "climbing"

    def do_keymaps(self, keymaps):
        self.actor.physics.climbing = True
        if Keymap.Up in keymaps:
            self.start_or_continue(actions.ClimbUp)
        elif Keymap.Down in keymaps:
            self.start_or_continue(actions.ClimbDown)

        if Keymap.Left in keymaps:
            self.start_or_continue(actions.ClimbLeft)
        elif Keymap.Right in keymaps:
            self.start_or_continue(actions.ClimbRight)

        if not keymaps:
            self.continue_current_action(stop_continuous=True)

        if not self.actor.physics.climbables:
            if self.executing_action:
                self.executing_action.on_stop()
                self.executing_action = None
            self.actor.stance.change_stance('idle')
            self.actor.physics.affected_by_gravity = True
            self.actor.physics.climbing = False


class Punching(Stance):
    name = "punching"

    def do_keymaps(self, keymaps):
        self.continue_current_action(stop_continuous=True)
        if self.executing_action is None:
            self.actor.stance.change_stance('idle')


class Dead(Stance):
    name = "dead"

    def do_keymaps(self, keymaps):
        if self.actor.physics.flying is True:
            self.actor.physics.flying = False
        # TODO Some enemies might want to rise from their graves
        if not self.actor.health.is_dead:
            self.actor.stance.change_stance('idle')


class Flying(Idle):
    name = "flying"

    def do_keymaps(self, keymaps):
        self.actor.physics.flying = True
        self.actor.physics.velocity_y /= 2
        if not keymaps:
            self.actor.physics.velocity_x /= 1.2
            self.continue_current_action(stop_continuous=True)
            self.actor.physics.velocity_y = 0

            return

        if Keymap.A in keymaps:
            self.start_or_continue(actions.Swoop)

        if Keymap.Up in keymaps:
            self.start_or_continue(actions.FlyUp)
        elif Keymap.Down in keymaps:
            self.start_or_continue(actions.FlyDown)

        if Keymap.Left in keymaps:
            self.start_or_continue(actions.FlyLeft)
        elif Keymap.Right in keymaps:
            self.start_or_continue(actions.FlyRight)
