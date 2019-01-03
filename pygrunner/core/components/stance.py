from pygrunner.core.components.base import Component


class Stance(Component):
    """
    Component keeping track of stances.
    """
    name = "stance"

    def __init__(self, default_stance, stances):
        super().__init__()
        self.default_stance = default_stance
        self.stances = stances
        self.current = default_stance

    def change_stance(self, new_stance_name):
        new_stance = self.stances.get(new_stance_name)
        if new_stance:
            self.current = new_stance
        self.current = self.default_stance


    def do_keymaps(self, keymaps):
        self.current.do_keymaps(keymaps)


    def reset(self):
        self.current = self.default_stance
