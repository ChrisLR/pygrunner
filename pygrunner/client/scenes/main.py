from pygrunner.client.scenes.base import Scene


class MainMenu(Scene):
    def __init__(self, inputs):
        super().__init__(inputs)

    def update(self, dt):
        all_keymaps = set()
        for input in self.inputs:
            keymap = input.get_keymaps()
            all_keymaps.update(keymap)
