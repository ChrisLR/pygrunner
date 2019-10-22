from pygrunner.core.components import listing
from pygrunner.core.components.base import Component
import math


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
        x, y = self._to_grid(host_location.x, host_location.y)
        y = int(y)
        frac, low_x = math.modf(x)
        low_x = int(low_x)
        collisions = []
        if frac <= 0.2:
            col = collision_map.check_collision(low_x, y + 1)
            if col:
                collisions.append(col)
        elif 0.2 < frac < 0.8:
            col_1 = collision_map.check_collision(low_x, y + 1)
            if col_1:
                collisions.append(col_1)
            col_2 = collision_map.check_collision(low_x + 1, y + 1)
            if col_2:
                collisions.append(col_2)
        elif frac >= 0.8:
            col = collision_map.check_collision(low_x + 1, y + 1)
            if col:
                collisions.append(col)


        return collisions

    @property
    def standing_on_solid(self):
        collisions = self.standing_on
        if collisions:
            return [c for c in collisions if c.physics.solid or c.physics.platform]

    @property
    def underneath(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        y = math.ceil(y)
        frac, low_x = math.modf(x)
        low_x = int(low_x)
        collisions = []
        if frac <= 0.2:
            col = collision_map.check_collision(low_x, y - 1)
            if col:
                collisions.append(col)
        elif 0.2 < frac < 0.8:
            col_1 = collision_map.check_collision(low_x, y - 1)
            if col_1:
                collisions.append(col_1)
            col_2 = collision_map.check_collision(low_x + 1, y - 1)
            if col_2:
                collisions.append(col_2)
        elif frac >= 0.8:
            col = collision_map.check_collision(low_x + 1, y - 1)
            if col:
                collisions.append(col)

        return collisions

    @property
    def underneath_solid(self):
        collisions = self.underneath
        if collisions:
            return [c for c in collisions if c.physics.solid]

    @property
    def right_collisions(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        x = int(x)
        frac, low_y = math.modf(y)
        low_y = int(low_y)
        collisions = []
        if frac <= 0.2:
            col = collision_map.check_collision(x + 1, low_y)
            if col:
                collisions.append(col)
        elif 0.2 < frac < 0.8:
            col_1 = collision_map.check_collision(x + 1, low_y)
            if col_1:
                collisions.append(col_1)
            col_2 = collision_map.check_collision(x + 1, low_y + 1)
            if col_2:
                collisions.append(col_2)
        elif frac >= 0.8:
            col = collision_map.check_collision(x + 1, low_y + 1)
            if col:
                collisions.append(col)

        return collisions

    @property
    def right_collisions_solid(self):
        collisions = self.right_collisions
        if collisions:
            return [c for c in collisions if c.physics.solid]

    @property
    def left_collisions(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        x = math.ceil(x)
        frac, low_y = math.modf(y)
        low_y = int(low_y)
        collisions = []
        if frac <= 0.2:
            col = collision_map.check_collision(x - 1, low_y)
            if col:
                collisions.append(col)
        elif 0.2 < frac < 0.8:
            col_1 = collision_map.check_collision(x - 1, low_y)
            if col_1:
                collisions.append(col_1)
            col_2 = collision_map.check_collision(x - 1, low_y + 1)
            if col_2:
                collisions.append(col_2)
        elif frac >= 0.8:
            col = collision_map.check_collision(x - 1, low_y + 1)
            if col:
                collisions.append(col)

        return collisions

    @property
    def left_collisions_solid(self):
        collisions = self.left_collisions
        if collisions:
            return [c for c in collisions if c.physics.solid]

    @property
    def center_collisions(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        coords = self._coords_from_fract(x, y, True, True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)

        return collisions

    @property
    def can_climb_up(self):
        collisions = []
        collisions.extend(self.center_collisions)
        collisions.extend(self.standing_on)
        if collisions:
            return [c for c in collisions if c.physics.climbable]

    @property
    def can_climb_down(self):
        collisions = []
        collisions.extend(self.center_collisions)
        collisions.extend(self.standing_on)
        if collisions:
            return [c for c in collisions if c.physics.climbable]

    def _to_grid(self, x, y):
        return x / 32, y / 32

    def _coords_from_fract(self, fixed_x, fixed_y, fract_x=False, fract_y=False, x_round_func=int, y_round_func=int):
        x = fixed_x
        x2 = None
        if fract_x:
            fx, x = math.modf(x)
            x, x2 = self._frac(x, fx)
        else:
            x = x_round_func(x)

        y = fixed_y
        y2 = None
        if fract_y:
            fy, y = math.modf(y)
            y, y2 = self._frac(y, fy)
        else:
            y = y_round_func(y)

        cols = []
        # TODO This is ugly
        if x:
            if y:
                cols.append((x, y))
            if y2:
                cols.append((x, y2))
        if x2:
            if y:
                cols.append((x2, y))
            if y2:
                cols.append((x2, y2))

        return cols

    def _frac(self, low, frac):
        low = int(low)
        if frac <= 0.2:
            return low, None
        elif 0.2 < frac < 0.8:
            return low, low + 1
        elif frac >= 0.8:
            return None, low + 1
        return low, low + 1
