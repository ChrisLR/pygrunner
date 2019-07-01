from pygrunner.core.components import listing
from pygrunner.core.components.base import Component


@listing.register
class StaticTriggers(Component):
    """
    A component holding any triggers that effect other objects when they intersect
    Useful for statics which are never calculated
    """

    name = "triggers"

    def __init__(self, triggerables=None):
        super().__init__()
        self.triggerables = triggerables or []

    def trigger(self, game_object, rect_name):
        for triggerable in self.triggerables:
            triggerable.trigger(game_object, rect_name)

    def add(self, triggerable):
        self.triggerables.append(triggerable)

    def reset(self):
        pass
