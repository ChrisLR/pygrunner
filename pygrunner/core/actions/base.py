import abc


class Action(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def can_execute(self, game_object):
        pass

    @abc.abstractmethod
    def execute(self, game_object):
        pass
