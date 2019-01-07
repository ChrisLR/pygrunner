import abc


class Action(metaclass=abc.ABCMeta):
    cancelable = True

    def __init__(self, actor):
        self.actor = actor

    @abc.abstractmethod
    def can_execute(self):
        pass

    @abc.abstractmethod
    def execute(self):
        pass

    def on_cancel(self):
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
        self.actor = None
