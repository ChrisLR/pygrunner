from pygrunner.core.components.base import Component


class Physics(Component):
    """
    This component holds data concerning the physics of an object.
    """

    name = "physics"

    def __init__(self, velocity_x = 0, velocity_y = 0, solid=True):
        super().__init__()
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.collisions = {}
        self.triggers = {}
        self.solid = solid
        self._initial_solid = solid

    def reset(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.collisions.clear()
        self.triggers = {}
        self.solid = self._initial_solid

    @property
    def bottom_collisions(self):
        return self.collisions["bottom"]

    @property
    def top_collisions(self):
        return self.collisions["top"]

    @property
    def right_collisions(self):
        return self.collisions["right"]

    @property
    def left_collisions(self):
        return self.collisions["left"]

    @property
    def center_collisions(self):
        return self.collisions["center"]

    @property
    def intersects(self):
        return self.collisions["intersects"]

    @property
    def bottom_triggers(self):
        return self.triggers["bottom"]

    @property
    def top_triggers(self):
        return self.triggers["top"]

    @property
    def right_triggers(self):
        return self.triggers["right"]

    @property
    def left_triggers(self):
        return self.triggers["left"]

    @property
    def center_triggers(self):
        return self.triggers["center"]
