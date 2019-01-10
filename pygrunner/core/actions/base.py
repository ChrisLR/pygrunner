import abc


class Action(metaclass=abc.ABCMeta):
    cancelable = True
    continuous = False

    def __init__(self, actor):
        self.actor = actor

    @abc.abstractmethod
    def can_execute(self):
        pass

    @abc.abstractmethod
    def execute(self):
        pass

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @property
    def finished(self):
        """
        This is ideal for continuous actions.
        Actions that are not cancelable will need to override this
        """
        return False

    def reset(self):
        # TODO If the action pool is shared, this will need to handle swapping actors
        pass
