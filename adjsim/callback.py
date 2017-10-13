
from . import utility

class Callback(object):
    def __init__(self):
        self.subscriptions = set()

    def register(self, callback):
        raise NotImplementedError

    def unregister(self, callback):
        raise NotImplementedError

    def is_registered(self, callback):
        raise NotImplementedError

    def __call__(self, callback):
        raise NotImplementedError

class SingleParameterCallback(Callback):

    def __init__(self):
        super().__init__()

    def register(self, callback):
        if not callable(callback):
            raise utility.InvalidCallbackException

        self.subscriptions.add(callback)

    def unregister(self, callback):
        if self.is_registered(callback):
            self.subscriptions.remove(callback)

    def is_registered(self, callback):
        return callback in self.subscriptions

    def __call__(self, parameter):
        for callback in self.subscriptions:
            callback(parameter)

class AgentChangedCallback(SingleParameterCallback):
    def __init__(self):
        super().__init__()


class SimulationMilestoneCallback(SingleParameterCallback):
    def __init__(self):
        super().__init__()