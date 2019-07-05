from pygrunner.core.keymap import Keymap
from pygrunner.gamedata.recipes.characters.base import Character


class FlyingAI(object):
    """
    This AI flies towards the nearest character once active
    """
    def __init__(self, host):
        self.host = host
        self.direction = 1
        self.keymaps = set()
        self.active = False

    def update(self):
        self.keymaps.clear()
        host_physics = self.host.physics
        characters = self.host.location.level.game_objects
        enemies = [char for char in characters if issubclass(char.recipe, Character)]
        host_point = self.host.location.point

        if enemies:
            closest = min(enemies, key=lambda c: c.location.point.distance_to(host_point))
            closest_point = closest.location.point
            min_dist = 200 if not self.active else 400
            if closest_point.distance_to(host_point) > min_dist:
                self.host.stance.do_keymaps(None)
                return
            else:
                self.active = True

            up, down, left, right = False, False, False, False
            delta_y = closest_point.y - host_point.y
            if delta_y < -10:
                up = True
            elif delta_y > 10:
                down = True

            if closest.location.x < host_point.x:
                left = True
            else:
                right = True
            self._move(left, right, up, down)

        intersects = host_physics.intersects
        if intersects:
            # TODO This must check alliance status, not recipe inheritance
            has_target = any(intersects)
            if has_target:
                return self._attack()

    def _attack(self):
        self.keymaps.add(Keymap.A)
        self.host.stance.do_keymaps(self.keymaps)

    def _move(self, left=False, right=False, up=False, down=False):
        # TODO This should be cleaner
        if left:
            self.keymaps.add(Keymap.Left)
        if right:
            self.keymaps.add(Keymap.Right)
        if up:
            self.keymaps.add(Keymap.Up)
        if down:
            self.keymaps.add(Keymap.Down)

        if not up and not down and (left or right):
            # TODO What we must do here is take a look at the next three tiles
            # TODO See if theres a hole and alter accordingly
            # TODO If there are none, simply retarget
            if left and self.host.physics.left_collisions:
                self.keymaps.add(Keymap.Up)
            elif right and self.host.physics.right_collisions:
                self.keymaps.add(Keymap.Up)

        if down and not (left or right):
            if self.host.physics.bottom_collisions:
                self.keymaps.remove(Keymap.Down)
        self.host.stance.do_keymaps(self.keymaps)

    def _get_directional_tile_collision(self, physics):
        if self.direction == 1:
            return physics.right_collisions
        else:
            return physics.left_collisions
