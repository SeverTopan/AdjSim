
from . import utility

class Callback(object):
    def __init__(self):
        self.subscriptions = []

    def register(self, callback):
        raise NotImplementedError

    def __call__(self, callback):
        raise NotImplementedError

class AgentChangedCallback(Callback):

    def __init__(self):
        super().__init__()

    def register(self, callback):
        if not callable(callback):
            raise utility.InvalidCallbackException

        self.subscriptions.append(callback)

    def __call__(self, agent):
        for callback in self.subscriptions:
            callback(agent)