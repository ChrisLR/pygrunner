from pygrunner.core.actions import WalkRight, WalkLeft, Jump, GlideLeft, GlideRight
from pygrunner.core.keymap import Keymap


class Stance(object):
    """
    Represents both the state of an object and the actions available to it
    """
    name = ""

    def __init__(self, actor):
        self.actor = actor
        self.executing_actions = {}

    def do_keymaps(self, keymaps):
        pass

    def start_or_continue(self, action_type, cancels=None):
        # TODO Executing actions that are not in keymaps
        # TODO Are not being updated here
        # TODO Will need to think about how actions stops others and how
        # TODO They will cancel
        if action_type is None:
            return

        if cancels is not None:
            could_cancel = True
            for cancelled_action_type in cancels:
                cancelled_action = self.executing_actions.get(cancelled_action_type)
                if cancelled_action is None:
                    continue

                if cancelled_action.cancelable:
                    cancelled_action.on_cancel()
                    del self.executing_actions[cancelled_action_type]
                else:
                    could_cancel = False
            if could_cancel is False:
                return

        just_started = False
        action = self.executing_actions.get(action_type)
        if action is None:
            just_started = True
            action = action_type(self.actor)

        if action.can_execute():
            self.executing_actions[action_type] = action
            if just_started:
                action.on_start()
            action.execute()
        else:
            action.on_stop()
            if not just_started:
                del self.executing_actions[action_type]

        if action.finished:
            action.on_stop()
            del self.executing_actions[action_type]


class Idle(Stance):
    name = "idle"

    def do_keymaps(self, keymaps):
        actor = self.actor
        if not keymaps:
            actor.display.play('idle')

        action_type = None
        cancels = None
        if Keymap.Left in keymaps:
            action_type = WalkLeft
            cancels = (WalkRight,)
        elif Keymap.Right in keymaps:
            action_type = WalkRight
            cancels = (WalkLeft,)

        self.start_or_continue(action_type, cancels)
        if Keymap.B in keymaps:
            self.start_or_continue(Jump)


class Running(Idle):
    name = "running"

    def do_keymaps(self, keymaps):
        actor = self.actor
        if not keymaps:
            actor.display.play('idle')
            actor.stance.change_stance('idle')
        else:
            super().do_keymaps(keymaps)


class Jumping(Stance):
    name = "jumping"

    def do_keymaps(self, keymaps):
        actor = self.actor
        if not keymaps:
            actor.display.play('idle')

        action_type = None
        cancels = None
        if Keymap.Left in keymaps:
            action_type = GlideLeft
            cancels = (GlideRight,)
        elif Keymap.Right in keymaps:
            action_type = GlideRight
            cancels = (GlideLeft,)

        self.start_or_continue(action_type, cancels)
        if self.actor.physics.bottom_collisions:
            self.actor.stance.change_stance('idle')
