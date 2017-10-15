"""Callback module.

This module contains callback objects, which are used to invoke user code at specific times during the simulation.

Designed and developed by Sever Topan.
"""

# Local.
from . import utility

class Callback(object):
    """The abstract base callback object. Callbacks are events that are called at specific times during the simulation.

    Attributes:
        subscriptions (set): The callables that will be called.
    """

    def __init__(self):
        self.subscriptions = set()

    def register(self, *args, **kwargs):
        """Registers a callback."""
        raise NotImplementedError

    def unregister(self, *args, **kwargs):
        """Unregisters a callback."""
        raise NotImplementedError

    def is_registered(self, callback):
        """Checks if a callback is registered."""
        raise NotImplementedError

    def __call__(self, callback):
        """Calls the callbacks."""
        raise NotImplementedError

class SingleParameterCallback(Callback):
    """Callback class for a single parameter callback.
    """

    def __init__(self):
        super().__init__()

    def register(self, callback):
        """Registers the callback.
        
        Args:
            callback (callable): the callback.
        """
        if not callable(callback):
            raise utility.InvalidCallbackException

        self.subscriptions.add(callback)

    def unregister(self, callback):
        """Unregisters the callback.
        
        Args:
            callback (callable): the callback.
        """
        if self.is_registered(callback):
            self.subscriptions.remove(callback)

    def is_registered(self, callback):
        """Checks callback registration.
        
        Args:
            callback (callable): the callback.

        Returns:
            True if the callback has previously been registered
        """
        return callback in self.subscriptions

    def __call__(self, parameter):
        """Calls all suscribed callables with the given parameter.
        
        Args:
            parameter (object): the callback parameter.
        """
        for callback in self.subscriptions:
            callback(parameter)

class AgentChangedCallback(SingleParameterCallback):
    """Callback specialization class for changed agent properties.
    """

    def __init__(self):
        super().__init__()


class SimulationMilestoneCallback(SingleParameterCallback):
    """Callback specialization class for simulation milestones.
    """

    def __init__(self):
        super().__init__()