from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class Physics(Component):
    """
    This component holds data concerning the physics of an object.
    """

    name = "physics"

    def __init__(self, velocity_x=0, velocity_y=0, solid=True, platform=False, climbable=False):
        super().__init__()
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.collisions = None
        self.intersects = None
        self.triggers = None
        self.solid = solid
        self._initial_solid = solid
        self.platform = platform
        self.climbable = climbable
        self.climbables = None
        self.climbing_down = False
        self.affected_by_gravity = True
        self.affected_by_velocity = True
        self.clear_collisions()

    def clear_collisions(self):
        self.collisions = {"bottom": set(), "top": set(), "left": set(), "right": set(), "center": set()}
        self.climbables = {"bottom": set(), "top": set(), "left": set(), "right": set(), "center": set()}
        self.intersects = set()
        self.triggers = {"bottom": set(), "top": set(), "left": set(), "right": set(), "center": set()}

    def reset(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.collisions.clear()
        self.triggers = {}
        self.solid = self._initial_solid
        self.climbing_down = False

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

    @property
    def bottom_climbables(self):
        return self.climbables["bottom"]

    @property
    def top_climbables(self):
        return self.climbables["top"]

    @property
    def right_climbables(self):
        return self.climbables["right"]

    @property
    def left_climbables(self):
        return self.climbables["left"]

    @property
    def center_climbables(self):
        return self.climbables["center"]
