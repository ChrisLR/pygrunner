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
        self.triggers = {}
        self.solid = self._initial_solid
        self.climbing_down = False

    @property
    def standing_on(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        # TODO Adding +1 here fixes foot stuck in floor
        # TODO So this hack is left here while we find out why
        x, y = self._to_grid(host_location.x, host_location.y + 1)
        coords = self._coords_from_fract(x, y, fract_x=True, y_round_func=math.ceil)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
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
        coords = self._coords_from_fract(x, y, fract_x=True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
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
        coords = self._coords_from_fract(x + 1, y, fract_y=True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
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
        coords = self._coords_from_fract(x - 1, y, fract_y=True, x_round_func=math.ceil)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
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
            climb_collisions = []
            for col in collisions:
                if col.physics.solid:
                    return False
                if col.physics.climbable:
                    climb_collisions.append(col)

            return climb_collisions

    def _to_grid(self, x, y):
        return x / 32, y / 32

    def _coords_from_fract(self, fixed_x, fixed_y, fract_x=False, fract_y=False,
                           x_round_func=int, y_round_func=int):
        """
        A method that returns tile coordinates that should be checked
        depending on the fractions and the rounding methods of given coordinates
        """

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
        if x is not None:
            if y is not None:
                cols.append((x, y))
            if y2 is not None:
                cols.append((x, y2))
        if x2 is not None:
            if y is not None:
                cols.append((x2, y))
            if y2 is not None:
                cols.append((x2, y2))

        return cols

    def _frac(self, low, frac):
        # This corresponds to the threshold in which we fetch more than one tile
        low = int(low)
        if frac <= 0.2:
            return low, None
        elif 0.2 < frac < 0.8:
            return low, low + 1
        elif frac >= 0.8:
            return None, low + 1
        return low, low + 1
