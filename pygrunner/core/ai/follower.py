from pygrunner.core.keymap import Keymap
from pygrunner.gamedata.recipes.characters.base import Character


class FollowerAI(object):
    """
    This AI followers a player as best it can.
    """
    def __init__(self, host):
        self.host = host
        self.direction = 1
        self.keymaps = set()

    def update(self):
        self.keymaps.clear()
        # TODO Here we must check distance with the closest player.
        # TODO If we are far away, we attempt a complex pathfind.
        # TODO If it fails, we stop any complex attempts for 10 seconds.
        # TODO If We are close, then we simply move in the appropriate direction.

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
