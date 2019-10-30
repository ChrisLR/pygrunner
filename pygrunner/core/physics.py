from pygrunner.core import util


class PhysicsEngine(object):
    def __init__(self, air_friction, gravity, ground_friction):
        self.air_friction = air_friction
        self.gravity = gravity
        # TODO We may want to take a tile's friction instead
        self.ground_friction = ground_friction

    def update(self, current_level):
        for game_object in current_level.game_objects:
            object_physics = game_object.physics
            object_physics.clear_collisions()
            speed_left_x = None
            speed_left_y = None
            finished = False
            while not finished:
                self.check_collisions(current_level, game_object)
                self._stop_static_colliding_objects(game_object, object_physics)
                speed_left_x, speed_left_y = self._move_object(game_object, object_physics, speed_left_x, speed_left_y)
                if abs(speed_left_x) <= 0.01 and abs(speed_left_y) <= 0.01:
                    finished = True
            self._apply_friction_and_gravity(object_physics)

    def check_collisions(self, current_level, game_object):
        self._set_object_collisions(current_level, game_object)

    def _move_object(self, game_object, object_physics, speed_left_x=None, speed_left_y=None):
        if object_physics.affected_by_velocity is False:
            return 0, 0

        velocity_x = object_physics.velocity_x if speed_left_x is None else speed_left_x
        velocity_y = object_physics.velocity_y if speed_left_y is None else speed_left_y

        direction_x = util.sign(object_physics.velocity_x)
        direction_y = util.sign(object_physics.velocity_y)
        if abs(velocity_x) >= 2:
            required_speed_x = abs(velocity_x / 2)
        else:
            required_speed_x = min(abs(direction_x), abs(velocity_x))

        speed_x = min(abs(direction_x), abs(velocity_x))

        if abs(velocity_y) >= 2:
            required_speed_y = abs(velocity_y / 2)
        else:
            required_speed_y = min(abs(direction_y), abs(velocity_y))

        speed_y = min(abs(direction_y), abs(velocity_y))

        # TODO We will want speed to vary in many situations
        # TODO To handle this, we will need to check collisions by projecting further
        # TODO To avoid sprites getting stuck
        game_object.location.add(speed_x * direction_x, speed_y * direction_y)

        return required_speed_x - speed_x, required_speed_y - speed_y

    def _stop_static_colliding_objects(self, game_object, object_physics):
        if object_physics.velocity_x > 0:
            if object_physics.right_collisions_solid:
                object_physics.velocity_x = 0
        elif object_physics.velocity_x < 0:
            if object_physics.left_collisions_solid:
                object_physics.velocity_x = 0

        if object_physics.velocity_y > 0:
            stand_solid_cols = object_physics.standing_on_solid
            if stand_solid_cols and not object_physics.climbing_down:
                object_physics.velocity_y = 0
                # TODO CHECK IF INSIDE TILE THEN PUSH UP
                if any(game_object.size.rectangle.bottom > col.location.y for col in stand_solid_cols):
                    game_object.location.add(0, -1)
        elif object_physics.velocity_y < 0:
            if object_physics.underneath_solid:
                object_physics.velocity_y = 0

    def _apply_friction_and_gravity(self, object_physics):
        if object_physics.velocity_x != 0:
            if not object_physics.flying and object_physics.standing_on_solid:
                object_physics.velocity_x /= (1 + self.ground_friction)
            else:
                object_physics.velocity_x /= (1 + self.air_friction)
            object_physics.velocity_x = object_physics.velocity_x if abs(object_physics.velocity_x) > 0.01 else 0

        if object_physics.velocity_y > 0 and object_physics.standing_on_solid:
            if not object_physics.climbing_down:
                object_physics.velocity_y = 0
        elif object_physics.affected_by_gravity:
            if -0.5 <= object_physics.velocity_y < 0.1:
                object_physics.velocity_y += 0.05
            else:
                accel = min(max(0.0, object_physics.velocity_y / 10), 10)
                object_physics.velocity_y += self.gravity + accel

    def _set_object_collisions(self, current_level, game_object):
        physics = game_object.physics
        # TODO This triggers center collisions, a bit off, could be better placed
        physics.trigger_center_collisions()

        object_intersects = physics.intersects
        for other_game_object in current_level.game_objects:
            if game_object is other_game_object:
                continue

            if other_game_object in object_intersects:
                continue

            first_rect = game_object.size.rectangle
            second_rect = other_game_object.size.rectangle
            if first_rect.intersects(second_rect):
                object_intersects.add(other_game_object)
                other_game_object.physics.intersects.add(game_object)
