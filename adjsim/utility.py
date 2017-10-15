"""Utility module.

This module contains miscellaneous utility objects and functions for use in adjsim.

Designed and developed by Sever Topan.
"""

# Standard.
import collections
import math

# Third Party.
import numpy as np

#-------------------------------------------------------------------------------
# Containers
#-------------------------------------------------------------------------------

class InheritableDict(collections.MutableMapping):
    """An inheritable dict interface.
    
    Overridable functions: __getitem__, __setitem__, __delitem__, __iter__, __len__.
    """

    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

class InheritableSet(collections.MutableSet):
    """An inheritable set interface.

    Overridable functions: __contains__, __iter__, __len__, add, discard.    
    """

    def __init__(self, *args, **kwargs):
        self._data = set(*args, **kwargs)

    def __contains__(self, value):
        return value in self._data

    def add(self, value):
        return self._data.add(value)

    def discard(self, value):
        return self._data.discard(value)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

#-------------------------------------------------------------------------------
# Exceptions
#-------------------------------------------------------------------------------

class SimulatonWorkflowException(Exception):

    MESSAGE = """Steps have been invoked on a non-running simulation.

    Please call 'start' in the simulation before 'step'. 
    Follow up simulation completion with a call to 'end'.
    """

    def __init__(self):
        super().__init__(SimulatonWorkflowException.MESSAGE)

class TrackerException(Exception):

    MESSAGE = """An Exception has occurred while calling a Tracker.

    Simulation.trackers should be a list of callable functors that inherit from Tracker.
    They must implement their __call__ method to take a Simulation object, and return the data that is desired.
    """

    def __init__(self):
        super().__init__(TrackerException.MESSAGE)


class InvalidAgentException(Exception):

    MESSAGE = """An agent must inherit from the Agent object."""

    def __init__(self):
        super().__init__(InvalidAgentException.MESSAGE)


class ActionException(Exception):

    MESSAGE = """An exception has occurred while calling an action.

    Action must be a callable that takes in a Simulation object.
    The callable return values will be ignored. Changes should be made in place in the Simulation object.
    Actions should set step_complete to True once no subsequent actions need be called.
    """

    def __init__(self):
        super().__init__(ActionException.MESSAGE)

class EndConditionException(Exception):

    MESSAGE = """An error has occurred while invoking the end_condition.

    An end condition must be a callable that takes in Simulation and returns a bool.
    """

    def __init__(self):
        super().__init__(EndConditionException.MESSAGE)

class InvalidCallbackException(Exception):

    MESSAGE = """A callback of invalid format has been supplied."""

    def __init__(self):
        super().__init__(InvalidCallbackException.MESSAGE)

class DecisionException(Exception):

    MESSAGE = """An error has occurred while invoking a decision module.

    Decision must be a callable takes in Simulation and a source agent. It should perform the
    neccessary computation for a given agent.
    """

    def __init__(self):
        super().__init__(DecisionException.MESSAGE)

class PerceptionException(Exception):

    MESSAGE = """An error has occurred while invoking a perception callable.
    
    Perception must be a callable that accepts simualtion and source agent as arguments.
    The perception function must return a tuple of types to be associated with a given agent state.
    """

    def __init__(self):
        super().__init__(PerceptionException.MESSAGE)

class LossException(Exception):

    MESSAGE = """An error has occurred while invoking a loss callable.
    
    Loss must be a callable that accepts simualtion and source agent as arguments.
    It must return a float-convertibale object. The lower the loss, the better the 
    action is considered to be.
    """

    def __init__(self):
        super().__init__(LossException.MESSAGE)

class MissingAttributeException(Exception):

    MESSAGE = """An attribute that was registered with the observation found is not present in the target agent."""

    def __init__(self):
        super().__init__(MissingAttributeException.MESSAGE)

class IndexInitializationException(Exception):

    MESSAGE = """The index has not been initialized prior to invocation of a query.
    
    Please call the index's 'initialize' method before querying it.
    """

    def __init__(self):
        super().__init__(IndexInitializationException.MESSAGE)
#-------------------------------------------------------------------------------
# Exposed Functions
#-------------------------------------------------------------------------------


def distance_square(lhs, rhs):
    """Obtain the square of the distance between two np.ndarray functions.
    
    Args:
        lhs (np.ndarray): the left hand side argument.
        rhs (np.ndarray): the right hand side argument.
    """
    return np.sum((rhs.pos - lhs.pos)**2)

def distance(lhs, rhs):
    """Obtain the the distance between two np.ndarray functions.
    
    Args:
        lhs (np.ndarray): the left hand side argument.
        rhs (np.ndarray): the right hand side argument.
    """
    return distance_square**0.5

def sigmoid(x):
    """Apply the sigmoid function.
    
    Args:
        x (float): The value to apply the sigmoid to.
    """
    return 1 / (1 + math.exp(-x))

def sigmoid_clamp(x, clamp_min, clamp_max):
    """Apply the sigmoid function and skew the results to vertiacally span between clamp_min and clamp_max.
    
    Args:
        x (float): The value to apply the sigmoid to.
        clamp_min (float): The value to skew the minimum to.
        clamp_max (float): The value to skew the maximum to.
    """
    clamp_delta = clamp_max - clamp_min
    return sigmoid(x)*clamp_delta - clamp_min
