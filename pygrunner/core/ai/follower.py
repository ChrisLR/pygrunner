from pygrunner.core.ai import common, pathfinding


class DumbFollowerAI(object):
    """
    This AI followers a player as best it can.
    """
    def __init__(self, host):
        self.host = host
        self.direction = 1

    def update(self):
        host = self.host
        if not host.game or not host.location.level:
            return

        closest_player = common.find_closest_player(host.game, host.location.point)
        keymaps = pathfinding.get_dumb_keymaps_to(host, closest_player.location.point, True, False, True, True)
        self.host.stance.do_keymaps(keymaps)

