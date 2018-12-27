class PlayerController(object):
    """
    This class links a Specific Player to an Actor.
    """
    def __init__(self, pid, game_input, actor=None):
        self.pid = pid
        self.game_input = game_input
        self.actor = actor

    def get_keymaps(self):
        return self.game_input.get_keymaps()

    def on_key_press(self, symbol, modifiers):
        self.game_input.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.game_input.on_key_release(symbol, modifiers)

    def update(self, dt):
        pass


class AIController(object):
    """
    This links an AI to an Actor
    """
    def __init__(self, actor, ai):
        self.actor = actor
        self.ai = ai

    def get_keymaps(self):
        return self.ai.get_keymaps()

    def update(self, dt):
        pass
