from pygrunner.core.actions import WalkRight, WalkLeft, Jump
from pygrunner.core.keymap import Keymap


class Stance(object):
    """
    Represents both the state of an object and the actions available to it
    """
    name = ""

    def __init__(self, action_pool, actor):
        self.action_pool = action_pool
        self.actor = actor
        self.executing_actions = {}

    def do_keymaps(self, keymaps):
        pass

    def start_or_continue(self, action_type, cancels=None):
        if action_type is None:
            return

        if cancels is not None:
            could_cancel = True
            for cancelled_action in cancels:
                if cancelled_action.cancelable:
                    cancelled_action.on_cancel()
                    del self.executing_actions[cancelled_action]
                else:
                    could_cancel = False
            if could_cancel is False:
                return

        just_started = False
        action = self.executing_actions.get(action_type)
        if action is None:
            just_started = True
            action = self.action_pool.get_or_create(action_type)

        if action.can_execute():
            if just_started:
                action.on_start()
                self.action_pool[action_type] = action
            action.execute()

        if action.finished:
            action.on_stop()
            del self.executing_actions[action_type]


class Idle(Stance):
    name = "Idle"

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


class Walking(Stance):
    name = "Walking"
