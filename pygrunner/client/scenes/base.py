class Scene(object):
    def __init__(self, inputs, window, game):
        self.inputs = inputs
        self.window = window
        self.game = game
        self.last_keymap_input = set()

    def on_draw(self):
        pass

    def update(self, dt):
        pass

    def get_all_input(self, only_new=True):
        current_keymap = set()
        for input in self.inputs:
            keymap = input.get_keymaps()
            current_keymap.update(keymap)

        if only_new is False:
            self.last_keymap_input = current_keymap
            return current_keymap
        new_keymap = current_keymap.difference(self.last_keymap_input)
        self.last_keymap_input = current_keymap

        return new_keymap
