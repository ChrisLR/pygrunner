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
        self.flying = False
        self.clear_collisions()

    def clear_collisions(self):
        self.intersects = set()

    def reset(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.collisions.clear()
        self.triggers = {}
        self.solid = self._initial_solid
        self.climbing_down = False

    @property
    def standing_on(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        return collision_map.check_collision(host_location.grid_x, host_location.grid_y + 1)

    @property
    def standing_on_solid(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        collision = collision_map.check_collision(host_location.grid_x, host_location.grid_y + 1)
        if collision and collision.physics.solid:
            return collision

    @property
    def underneath(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        return collision_map.check_collision(host_location.grid_x, host_location.grid_y - 1)

    @property
    def underneath_solid(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        collision = collision_map.check_collision(host_location.grid_x, host_location.grid_y - 1)
        if collision and collision.physics.solid:
            return collision

    @property
    def right_collisions(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        return collision_map.check_collision(host_location.grid_x + 1, host_location.grid_y)

    @property
    def left_collisions(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        return collision_map.check_collision(host_location.grid_x - 1, host_location.grid_y)

    @property
    def center_collisions(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        return collision_map.check_collision(host_location.grid_x, host_location.grid_y)

    @property
    def can_climb(self):
        collision = self.center_collisions
        if collision and collision.physics.climbable:
            return collision
