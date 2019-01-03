import abc



class Component(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def name(cls):
        return ""

    def __init__(self):
        self.host = None

    @abc.abstractmethod
    def reset(self):
        pass

    def register(self, host):
        self.host = host

    def update(self):
        pass