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
        self.data = None

    def __call__(self, simulation):
        return NotImplementedError

    def plot(self):
        return NotImplementedError


class AgentCountTracker(Tracker):

    def __init__(self):
        super().__init__()
        self.data = []

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

class AgentTypeCountTracker(Tracker):

    def __init__(self):
        super().__init__()
        self.data = {}

    def __call__(self, simulation):
        # Update the count of all known types to the current timestep.
        # This handles the case where population dips to zero for a known type.
        for agent_type_count in self.data.values():
            while len(agent_type_count) < simulation.time + 1:
                agent_type_count.append(0)

        for agent in simulation.agents:
            # If type is not present, initialize list entry.
            if not type(agent) in self.data:
                self.data[type(agent)] = [0 for i in range(simulation.time + 1)]

            # Increment the counter.
            self.data[type(agent)][-1] += 1

    def plot(self):
        pyplot.style.use('ggplot')

        for agent_type, agent_type_count in self.data.items():
            typename = agent_type.__name__ + " Agent Count"
            line, = pyplot.plot(agent_type_count, label=typename)
            line.set_antialiased(True)

        pyplot.xlabel('Timestep')
        pyplot.ylabel('Agent Count')
        pyplot.title('Agent Count by Type Over Time')
        pyplot.legend()

        pyplot.show()