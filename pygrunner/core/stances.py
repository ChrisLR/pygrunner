class Stance(object):
    """
    Represents both the state of an object and the actions available to it
    """
    def __init__(self, actions, name):
        self.actions = actions
        self.name = name
