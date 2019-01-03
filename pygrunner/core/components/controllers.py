from pygrunner.core.components.base import Component


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

    def on_key_press(self, symbol, modifiers):
        self.game_input.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.game_input.on_key_release(symbol, modifiers)

    def update(self):
        keymaps = self.get_keymaps()
        if keymaps:
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
        # TODO Ais
        #return self.ai.get_keymaps()
        pass

    def update(self):
        keymaps = self.get_keymaps()
        if keymaps:
            self.host.stance.do_keymaps(keymaps)
