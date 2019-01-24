from pygrunner.core.componentholder import ComponentHolder


class GameObject(ComponentHolder):
    """
    An Object with a presence in-game

    This object has at a minimum a display, location, physics and size
    """
    def __init__(self, name, display, location, physics, size, recipe=None):
        super().__init__()
        self.name = name
        self.add_components((display, location, size, physics))
        self.flipped = False
        self.recipe = recipe
        self.recycle = False


class StaticObject(GameObject):
    """
    A Special Game Object that is not meant to move.

    It will make several calculations such as collisions easier
    at the cost of a more intensive move cost.
    """

    def __init__(self, name, display, location, physics, size, recipe=None):
        super().__init__(name, display, location, physics, size, recipe)


class Actor(GameObject):
    """
    A controllable object with a presence in-game

    This object has at a minimum a controller, display, location, stance
    """
    def __init__(self, name, controller, display, location, physics, size, stance, recipe):
        super().__init__(name, display, location, physics, size, recipe)
        self.add_components((controller, stance))
