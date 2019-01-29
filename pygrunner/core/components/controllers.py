from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class PlayerController(Component):
    """
    This class links a Specific Player to an Actor.
    """
    name = "controller"

    def __init__(self, pid, game_input):
        super().__init__()
        self.pid = pid
        self.game_input = game_input

    def get_keymaps(self):
        return self.game_input.get_keymaps()

    def reset(self):
        # TODO This might need a proper reset
        pass

    def update(self):
        keymaps = self.get_keymaps()
        self.host.stance.do_keymaps(keymaps)


class AIController(Component):
    """
    This links an AI to an Actor
    """
    name = "controller"

    def __init__(self, ai):
        super().__init__()
        self.ai = ai

    def get_keymaps(self):
        pass

    def update(self):
        if self.ai:
            self.ai.update()

    def reset(self):
        # TODO AIs will have state to reset
        pass
