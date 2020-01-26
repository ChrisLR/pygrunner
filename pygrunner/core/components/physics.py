import math

from pygrunner.core.components import listing
from pygrunner.core.components.base import Component

UNSET = object()


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
        self.climbing = False
        self.climbing_down = False
        self.affected_by_gravity = True
        self.affected_by_velocity = True
        self.flying = False
        self.clear_collisions()
        self._standing_on = UNSET
        self._standing_on_solid = UNSET
        self._underneath = UNSET
        self._underneath_solid = UNSET
        self._right_collisions = UNSET
        self._right_collisions_solid = UNSET
        self._left_collisions = UNSET
        self._left_collisions_solid = UNSET
        self._center_collisions = UNSET
        self._can_climb_up = UNSET
        self._can_climb_down = UNSET

    def clear_collisions(self):
        self.intersects = set()

    def clear_collision_cache(self):
        # I know using a cachedproperty would save a lot of manual work
        # But this way should perform more and not many properties will be added here
        self._standing_on = UNSET
        self._standing_on_solid = UNSET
        self._underneath = UNSET
        self._underneath_solid = UNSET
        self._right_collisions = UNSET
        self._right_collisions_solid = UNSET
        self._left_collisions = UNSET
        self._left_collisions_solid = UNSET
        self._center_collisions = UNSET
        self._can_climb_up = UNSET
        self._can_climb_down = UNSET
        self._bottom_right = UNSET
        self._bottom_left = UNSET
        self._top_right = UNSET
        self._top_left = UNSET

    def reset(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.triggers = {}
        self.solid = self._initial_solid
        self.climbing_down = False

    def knockback(self, x=0, y=0):
        if self.climbing or self.climbing_down:
            return
        self.velocity_x += x
        self.velocity_y += y

    @property
    def top_left(self):
        if self._top_left is not UNSET:
            return self._top_left

        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        coords = self._coords_from_fract(x - 1, y, fract_x=True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)

        self._top_left = collisions

        return collisions

    @property
    def top_right(self):
        if self._top_right is not UNSET:
            return self._top_right

        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        coords = self._coords_from_fract(x + 1, y, fract_x=True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)

        self._top_right = collisions

        return collisions

    @property
    def bottom_left(self):
        if self._bottom_left is not UNSET:
            return self._bottom_left

        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        # TODO Adding +1 here fixes foot stuck in floor
        # TODO So this hack is left here while we find out why
        x, y = self._to_grid(host_location.x - 1, host_location.y + 1)
        coords = self._coords_from_fract(x, y, fract_x=True, y_round_func=math.ceil)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)

        self._bottom_left = collisions

        return collisions

    @property
    def bottom_right(self):
        if self._bottom_right is not UNSET:
            return self._bottom_right

        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        # TODO Adding +1 here fixes foot stuck in floor
        # TODO So this hack is left here while we find out why
        x, y = self._to_grid(host_location.x + 1, host_location.y + 1)
        coords = self._coords_from_fract(x, y, fract_x=True, y_round_func=math.ceil)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)

        self._bottom_right = collisions

        return collisions

    @property
    def standing_on(self):
        if self._standing_on is not UNSET:
            return self._standing_on

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
                if col.triggers:
                    col.triggers.trigger(self.host, "standing_on")

        self._standing_on = collisions

        return collisions

    @property
    def standing_on_solid(self):
        if self._standing_on_solid is not UNSET:
            return self._standing_on_solid

        collisions = self.standing_on
        if collisions:
            collisions = [c for c in collisions if c.physics.solid or c.physics.platform]

        self._standing_on_solid = collisions

        return collisions

    @property
    def underneath(self):
        if self._underneath is not UNSET:
            return self._underneath

        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        coords = self._coords_from_fract(x, y, fract_x=True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)
                if col.triggers:
                    col.triggers.trigger(self.host, "underneath")

        self._underneath = collisions

        return collisions

    @property
    def underneath_solid(self):
        if self._underneath_solid is not UNSET:
            return self._underneath_solid

        collisions = self.underneath
        if collisions:
            collisions = [c for c in collisions if c.physics.solid]

        self._underneath_solid = collisions

        return collisions

    @property
    def right_collisions(self):
        if self._right_collisions is not UNSET:
            return self._right_collisions

        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        coords = self._coords_from_fract(x + 1, y, fract_y=True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)
                if col.triggers:
                    col.triggers.trigger(self.host, "right")

        self._right_collisions = collisions

        return collisions

    @property
    def right_collisions_solid(self):
        if self._right_collisions_solid is not UNSET:
            return self._right_collisions_solid

        collisions = self.right_collisions
        if collisions:
            collisions = [c for c in collisions if c.physics.solid]

        self._right_collisions_solid = collisions

        return collisions

    @property
    def left_collisions(self):
        if self._left_collisions is not UNSET:
            return self._left_collisions

        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        coords = self._coords_from_fract(x - 1, y, fract_y=True, x_round_func=math.ceil)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)
                if col.triggers:
                    col.triggers.trigger(self.host, "left")

        self._left_collisions = collisions

        return collisions

    @property
    def left_collisions_solid(self):
        if self._left_collisions_solid is not UNSET:
            return self._left_collisions_solid

        collisions = self.left_collisions
        if collisions:
            collisions = [c for c in collisions if c.physics.solid]

        self._left_collisions_solid = collisions

        return collisions

    @property
    def center_collisions(self):
        if self._center_collisions is not UNSET:
            return self._center_collisions

        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        coords = self._coords_from_fract(x, y, True, True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)
                if col.triggers:
                    col.triggers.trigger(self.host, "center")

        self._center_collisions = collisions

        return collisions

    @property
    def can_climb_up(self):
        if self._can_climb_up is not UNSET:
            return self._can_climb_up

        collisions = []
        collisions.extend(self.center_collisions)
        collisions.extend(self.standing_on)
        if collisions:
            collisions = [c for c in collisions if c.physics.climbable]

        self._can_climb_up = collisions

        return collisions

    @property
    def can_climb_down(self):
        if self._can_climb_down is not UNSET:
            return self._can_climb_down

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

            collisions = climb_collisions

        self._can_climb_down = collisions

        return collisions

    def trigger_center_collisions(self):
        host_location = self.host.location
        collision_map = host_location.level.static_collision_map
        x, y = self._to_grid(host_location.x, host_location.y)
        coords = self._coords_from_fract(x, y, True, True)
        collisions = []
        for coord in coords:
            col = collision_map.check_collision(*coord)
            if col:
                collisions.append(col)
                if col.triggers:
                    col.triggers.trigger(self.host, "center")

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
