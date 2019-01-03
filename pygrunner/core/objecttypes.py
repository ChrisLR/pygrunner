class GameObject(object):
    """
    An Object with a presence in-game

    This object has at a minimum a display, location, physics and properties
    """
    def __init__(self, name, display, location, physics, properties, size):
        self.name = name
        self.display = display
        self.location = location
        self.physics = physics
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

    def __init__(self, name, display, location, physics, properties, size):
        super().__init__(name, display, location, physics, properties, size)


class Actor(GameObject):
    """
    A controllable object with a presence in-game

    This object has at a minimum a controller, display, location, properties, stance
    """
    def __init__(self, name, controller, display, location, physics, properties, size, stance):
        super().__init__(name, display, location, physics, properties, size)
        self.controller = controller
        self.stance = stance

    def update(self):
        self.controller.update()
        super().update()
