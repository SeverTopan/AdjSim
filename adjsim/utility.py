
import collections
import math

import numpy as np

#-------------------------------------------------------------------------------
# Containers
#-------------------------------------------------------------------------------

class InheritableDict(collections.MutableMapping):
    """A dict interface.
    
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
    """A set interface.

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

class InvalidTrackerException(Exception):

    MESSAGE = """A tracker of invalid format has been supplied.

        Simulation.trackers should be a list of callable functors that inherit from Tracker.
        They must implement their __call__ method to take a Simulation object, and return the data that is desired.
        """

    def __init__(self):
        super().__init__(InvalidTrackerException.MESSAGE)


class InvalidAgentException(Exception):

    MESSAGE = """An agent must inherit from the Agent object."""

    def __init__(self):
        super().__init__(InvalidAgentException.MESSAGE)


class InvalidActionException(Exception):

    MESSAGE = """An action of invalid format has been supplied.

        Action must be a callable that takes in a Simulation object.
        The callable return values will be ignored. Changes should be made in place in the Simulation object."""

    def __init__(self):
        super().__init__(InvalidActionException.MESSAGE)

class InvalidEndConditionException(Exception):

    MESSAGE = """An end condition of invalid format has been supplied.

        An end condition must be a callable that takes in Simulation and returns a bool."""

    def __init__(self):
        super().__init__(InvalidEndConditionException.MESSAGE)

class InvalidCallbackException(Exception):

    MESSAGE = """A callback of invalid format has been supplied."""

    def __init__(self):
        super().__init__(InvalidCallbackException.MESSAGE)

class InvalidDecisionException(Exception):

    MESSAGE = """A Decision Module of invalid format has been supplied.

        decision must be a callable takes in Simulation and a source agent."""

    def __init__(self):
        super().__init__(InvalidDecisionException.MESSAGE)

class InvalidPerceptionException(Exception):

    MESSAGE = """A perception function of invalid format has been supplied. 
    
        perception must be a callable that accepts simualtion and source agent as arguments.
        The perception function must return a tuple of types to be associated with a given agent state."""

    def __init__(self):
        super().__init__(InvalidPerceptionException.MESSAGE)

class InvalidLossException(Exception):

    MESSAGE = """A loss function of invalid format has been supplied. 
    
        loss must be a callable that accepts simualtion and source agent as arguments."""

    def __init__(self):
        super().__init__(InvalidLossException.MESSAGE)

class MissingAttributeException(Exception):

    MESSAGE = """An attribute that was registered with the observation found is not present in the target agent."""

    def __init__(self):
        super().__init__(MissingAttributeException.MESSAGE)

class IndexInitializationException(Exception):

    MESSAGE = """The index has not been initialized prior to invocation of a query.
    
        Please call the index's 'initialize' method before querying it."""

    def __init__(self):
        super().__init__(IndexInitializationException.MESSAGE)
#-------------------------------------------------------------------------------
# Exposed Functions
#-------------------------------------------------------------------------------


def distance_square(lhs, rhs):
    return np.sum((rhs.pos - lhs.pos)**2)

def distance(lhs, rhs):
    return distance_square**0.5

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_clamp(x, clamp_min, clamp_max):
    clamp_delta = clamp_max - clamp_min
    return sigmoid(x)*clamp_delta - clamp_min
