from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
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

    def add_stance(self, stance):
        self.stances[stance.name] = stance

    def update(self):
        pass

    def change_stance(self, next_stance_name):
        if next_stance_name and (self.current and next_stance_name != self.current.name):
            new_stance = self.stances.get(next_stance_name)
            # TODO This indicates that actions should be shared
            if new_stance and self.current:
                new_stance.executing_action = self.current.executing_action
            if new_stance:
                self.current = new_stance
            else:
                self.current = self.stances.get(self.default_stance.name)

    def do_keymaps(self, keymaps):
        self.current.do_keymaps(keymaps)

    def register(self, host):
        super().register(host)
        self.stances = {stance.name: stance(host) for stance in self.stances}
        self.current = self.stances.get(self.default_stance.name)

    def reset(self):
        self.current = self.default_stance
