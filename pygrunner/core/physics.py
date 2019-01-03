class PhysicsEngine(object):
    def __init__(self, air_friction, gravity, ground_friction):
        self.air_friction = air_friction
        self.gravity = gravity
        self.ground_friction = ground_friction

    def update(self, current_level):
        for game_object in current_level.game_objects:
            self.check_collisions(current_level, game_object)
            self.move_object(current_level, game_object)

    def check_collisions(self, current_level, game_object):
        all_object_collisions = set()
        self._set_object_collisions(all_object_collisions, current_level, game_object)
        self._set_static_collisions(current_level, game_object)

    def move_object(self, current_level, game_object):
        # TODO Move the object, update the velocity and gravity depending on collisions and frictions
        pass


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
            "bottom", game_object.size.bottom_rectangle,
            "right", game_object.size.right_rectangle,
            "left", game_object.size.left_rectangle,
            "top", game_object.size.top_rectangle,
        ]

        for name, rectangle in rectangles:
            collisions = static_map.check_collision_rect(rectangle)
            game_object.physics.collisions[name] = collisions