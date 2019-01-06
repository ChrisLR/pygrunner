from pygrunner.core.actions import WalkRight, WalkLeft, Jump
from pygrunner.core.keymap import Keymap


class Stance(object):
    """
    Represents both the state of an object and the actions available to it
    """
    actions = None
    name = ""

    @classmethod
    def do_keymaps(cls, game_object, keymaps):
        pass


class Idle(Stance):
    actions = WalkRight, WalkLeft
    name = "Idle"

    @classmethod
    def do_keymaps(cls, game_object, keymaps):
        if Keymap.Left in keymaps:
            if WalkLeft.can_execute(game_object):
                WalkLeft.execute(game_object)
        elif Keymap.Right in keymaps:
            if WalkRight.can_execute(game_object):
                WalkRight.execute(game_object)

        if Keymap.B in keymaps:
            if Jump.can_execute(game_object):
                Jump.execute(game_object)


class Walking(Stance):
    actions = WalkRight, WalkLeft
    name = "Walking"
