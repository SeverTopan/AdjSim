"""

"""

import abc

# third party
from matplotlib import pyplot
import numpy as np

# local
from . import decision
from . import utility 

class Tracker(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.data = []

    @abc.abstractmethod
    def __call__(self, simulation):
        return NotImplementedError


class AgentCountTracker(Tracker):

    def __call__(self, simulation):
        return len(simulation.agents)