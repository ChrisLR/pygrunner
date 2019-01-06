import abc


class Action(metaclass=abc.ABCMeta):
    # TODO Actions are better with instances but that will require pools
    @classmethod
    @abc.abstractmethod
    def can_execute(cls, game_object):
        pass

    @classmethod
    @abc.abstractmethod
    def execute(cls, game_object):
        pass
