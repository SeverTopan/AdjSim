"""

"""


# third party
from matplotlib import pyplot
import numpy as np

# local
from . import decision
from . import utility 

class Tracker(object):

    def __init__(self):
        self.data = []

    def __call__(self, simulation):
        return NotImplementedError

    def plot(self):
        return NotImplementedError


class AgentCountTracker(Tracker):

    def __call__(self, simulation):
        self.data.append(len(simulation.agents))

    def plot(self):
        pyplot.style.use('ggplot')

        line, = pyplot.plot(self.data, label="Global Agent Count")
        line.set_antialiased(True)

        pyplot.xlabel('Timestep')
        pyplot.ylabel('Agent Count')
        pyplot.title('Global Agent Count Over Time')
        pyplot.legend()

        pyplot.show()