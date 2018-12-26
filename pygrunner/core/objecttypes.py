class GameObject(object):
    """
    An Object with a presence in-game

    This object has at a minimum a display, location and properties
    """
    def __init__(self, name, display, location, properties, size):
        self.name = name
        self.display = display
        self.location = location
        self.properties = properties
        self.size = size

    def update(self):
        self.display.update()
        self.location.update()
        self.properties.update()


class StaticObject(GameObject):
    """
    A Special Game Object that is not meant to move.

    It will make several calculations such as collisions easier
    at the cost of a more intensive move cost.
    """

    def __init__(self, name, display, location, properties, size):
        super().__init__(name, display, location, properties, size)


class Actor(GameObject):
    """
    A controllable object with a presence in-game

    This object has at a minimum an action_set, controller, display, location, properties
    """
    def __init__(self, name, action_set, controller, display, location, properties, size):
        super().__init__(name, display, location, properties, size)
        self.action_set = action_set
        self.controller = controller

    def update(self):
        self.controller.update()
        super().update()
