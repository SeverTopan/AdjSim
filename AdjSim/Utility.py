
import collections
import numpy as np

#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------

# colors
RED_LIGHT = '#ff6961'
RED_DARK = '#c23b22'
BLUE_LIGHT = '#aec6cf'
BLUE_DARK = '#779ecb'
GREEN = '#aadd77'
PINK = '#dea5a4'
WHITE = '#f0ead6'
BROWN_DARK = '#64503f'
BROWN_LIGHT = '#a08269'
GREY = '#cfcfc4'
ORANGE = '#ff9447'

COLORS = [RED_LIGHT, RED_DARK, BLUE_LIGHT, BLUE_DARK, GREEN, PINK, WHITE]

# default ellipse object parameters
DEFAULT_OBJECT_RADIUS = 25
DEFAULT_OBJECT_BORDER_WIDTH = 2

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

        action must be a callable that takes in a Simulation object.
        The callable return values will be ignored. Changes should be made in place in the Simulation object."""
    
    def __init__(self):
        super().__init__(InvalidActionException.MESSAGE)

class InvalidEndConditionException(Exception):

    MESSAGE = """An end condition of invalid format has been supplied.

        an end condition must be a callable that takes in Simulation and returns a bool."""
    
    def __init__(self):
        super().__init__(InvalidEndConditionException.MESSAGE)

class InvalidCallbackException(Exception):

    MESSAGE = """A callback of invalid format has been supplied.

        a callback must be a callable that takes in Simulation and returns a bool."""
    
    def __init__(self):
        super().__init__(InvalidCallbackException.MESSAGE)


#-------------------------------------------------------------------------------
# Exposed Functions
#-------------------------------------------------------------------------------


def distance_square(lhs, rhs):
    return np.sum((rhs.pos - lhs.pos)**2)
