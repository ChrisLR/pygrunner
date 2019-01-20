class GameObject(object):
    """
    An Object with a presence in-game

    This object has at a minimum a display, location, physics and size
    """
    def __init__(self, name, display, location, physics, size, recipe=None):
        self.name = name
        self.display = display
        self.location = location
        self.physics = physics
        self.size = size
        self.display.register(self)
        self.location.register(self)
        self.physics.register(self)
        self.size.register(self)
        self.flipped = False
        self.recipe = recipe

    def update(self, dt):
        self.display.update()
        self.location.update()
        self.size.update()


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
        self.controller = controller
        self.stance = stance
        self.controller.register(self)
        self.stance.register(self)

    def update(self, dt):
        self.stance.update()
        self.controller.update()
        super().update(dt)
