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
            self.check_collisions(current_level, game_object)
            self._stop_static_colliding_objects(object_physics)
            self._move_object(game_object, object_physics)
            self._apply_friction_and_gravity(object_physics)

    def check_collisions(self, current_level, game_object):
        all_object_collisions = set()
        self._set_object_collisions(all_object_collisions, current_level, game_object)
        self._set_static_collisions(current_level, game_object)

    def _move_object(self, game_object, object_physics):
        direction_x = util.sign(object_physics.velocity_x)
        direction_y = util.sign(object_physics.velocity_y)

        speed_x = min(abs(direction_x), abs(object_physics.velocity_x))
        speed_y = min(abs(direction_y), abs(object_physics.velocity_y))
        # TODO We will want speed to vary in many situations
        # TODO To handle this, we will need to check collisions by projecting further
        # TODO To avoid sprites getting stuck
        game_object.location.add(speed_x * direction_x, speed_y * direction_y)

    def _stop_static_colliding_objects(self, object_physics):
        if object_physics.velocity_x > 0:
            if object_physics.right_collisions:
                object_physics.velocity_x = 0
        elif object_physics.velocity_x < 0:
            if object_physics.left_collisions:
                object_physics.velocity_x = 0

        if object_physics.velocity_y > 0:
            if object_physics.bottom_collisions:
                object_physics.velocity_y = 0
        elif object_physics.velocity_y < 0:
            if object_physics.top_collisions:
                object_physics.velocity_y = 0

    def _apply_friction_and_gravity(self, object_physics):
        if object_physics.velocity_x != 0:
            if object_physics.bottom_collisions:
                object_physics.velocity_x /= (1 + self.ground_friction)
            else:
                object_physics.velocity_x /= (1 + self.air_friction)
            object_physics.velocity_x = object_physics.velocity_x if abs(object_physics.velocity_x) > 0.01 else 0

        if object_physics.velocity_y > 0 and object_physics.bottom_collisions:
            object_physics.velocity_y = 0
        else:
            if -0.5 <= object_physics.velocity_y < 0.1:
                object_physics.velocity_y += 0.05
            else:
                object_physics.velocity_y += self.gravity

    def _set_object_collisions(self, all_object_collisions, current_level, game_object):
        intersect_collisions = []
        for other_game_object in current_level.game_objects:
            if game_object is other_game_object:
                continue

            collision_tuple = game_object, other_game_object
            if collision_tuple in all_object_collisions:
                intersect_collisions.append(collision_tuple)
                continue

            first_rect = game_object.size.rectangle
            second_rect = other_game_object.size.rectangle
            if first_rect.intersects(second_rect):
                all_object_collisions.add(collision_tuple)
                intersect_collisions.append(collision_tuple)

            game_object.physics.collisions["intersect"] = intersect_collisions

    def _set_static_collisions(self, current_level, game_object):
        static_map = current_level.static_collision_map
        rectangles = [
            ("bottom", game_object.size.bottom_rectangle),
            ("right", game_object.size.right_rectangle),
            ("left", game_object.size.left_rectangle),
            ("top", game_object.size.top_rectangle),
            ("center", game_object.size.center_rectangle)
        ]

        for name, rectangle in rectangles:
            collisions = static_map.check_collision_rect(rectangle)
            solids = {collision for collision in collisions if collision.physics.solid}
            non_solids = collisions.difference(solids)
            game_object.physics.collisions[name] = solids
            game_object.physics.triggers[name] = non_solids
            if name == "bottom":
                platforms = {collision for collision in non_solids if collision.physics.platform}
                game_object.physics.collisions[name].update(platforms)
