from pygrunner.core.actions import WalkRight, WalkLeft


class Stance(object):
    """
    Represents both the state of an object and the actions available to it
    """
    actions = None
    name = ""


class Idle(Stance):
    actions = WalkRight, WalkLeft
    name = "Idle"


class Walking(Stance):
    actions = WalkRight, WalkLeft
    name = "Walking"
