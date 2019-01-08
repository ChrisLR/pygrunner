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
        self.current = None
        self.next_stance_name = None

    def update(self):
        if self.next_stance_name:
            next_stance_name = self.next_stance_name
            self.next_stance_name = None
            print('Changing stance to %s' % next_stance_name)
            new_stance = self.stances.get(next_stance_name)
            if new_stance:
                self.current = new_stance
            else:
                self.current = self.stances.get(self.default_stance.name)

    def change_stance(self, new_stance_name):
        self.next_stance_name = new_stance_name

    def do_keymaps(self, keymaps):
        self.current.do_keymaps(keymaps)

    def register(self, host):
        super().register(host)
        self.stances = {stance.name: stance(host) for stance in self.stances}
        self.current = self.stances.get(self.default_stance.name)

    def reset(self):
        self.current = self.default_stance
