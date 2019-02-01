from pygrunner.core.keymap import Keymap
from pygrunner.gamedata.recipes.characters.base import Character


class ZombieAI(object):
    """
    This AI mindlessly walks left or right until it hits a wall or a ledge.
    If it intersects with a Character it attacks
    """
    def __init__(self, host):
        self.host = host
        self.direction = 1
        self.keymaps = set()

    def update(self):
        self.keymaps.clear()
        host_physics = self.host.physics
        static_collisions = self._get_directional_tile_collision(host_physics)
        if static_collisions:
            self.direction *= -1
            return
        # TODO We need to get a bottom corner to detect and change directions instead of falling

        intersects = host_physics.intersects
        if intersects:
            # TODO This must check alliance status, not recipe inheritance
            has_target = any(char for char in intersects if issubclass(char.recipe, Character))
            if has_target:
                return self._attack()
        return self._move()

    def _attack(self):
        self.keymaps.add(Keymap.A)
        self.host.stance.do_keymaps(self.keymaps)

    def _move(self):
        # TODO This should be cleaner
        if self.direction == 1:
            self.keymaps.add(Keymap.Right)
        else:
            self.keymaps.add(Keymap.Left)
        self.host.stance.do_keymaps(self.keymaps)

    def _get_directional_tile_collision(self, physics):
        if self.direction == 1:
            return physics.right_collisions
        else:
            return physics.left_collisions
