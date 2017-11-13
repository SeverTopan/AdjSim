"""Analysis module.

This module contains trackers, which are used to extract data from the simulation at
simulation runtime.

Designed and developed by Sever Topan.
"""


# Third Party.
from matplotlib import pyplot
import numpy as np

# Local.
from . import decision
from . import utility 

class Tracker(object):
    """The abstract base tracker object. Trackers used to analyze the simulation.

    All trackers must derive from this object. Trackers obtain data from the simulation after each
    iteration and must store the obtained data in their data attribute. This is done by implementing the
    __call__ method, and storing relevant data from the call method into the tracker's data attribute.

    Attributes:
        data (object): the data to store in the tracker.
    """

    def __init__(self):
        self.data = None

    def __call__(self, simulation):
        """Tracks data from the simulation.
        
        This functor call method is called after each simulation step. Desired data must be stored into
        the tracker's data attribute.

        Args:
            simulation (Simulation): The simulation to track.
        """
        return NotImplementedError

    def plot(self):
        """Plots the data attribute using pyplot."""
        return NotImplementedError


class AgentCountTracker(Tracker):
    """Counts the number of agents at each timestep.

    Attributes:
        data (list): The number of agents at each timestep.
    """

    def __init__(self):
        super().__init__()
        self.data = []

    def __call__(self, simulation):
        """Tracks the number of agents in the simulation."""
        self.data.append(len(simulation.agents))

    def plot(self):
        """Plots the data attribute using pyplot."""
        pyplot.style.use('ggplot')

        line, = pyplot.plot(self.data, label="Global Agent Count")
        line.set_antialiased(True)

        pyplot.xlabel('Timestep')
        pyplot.ylabel('Agent Count')
        pyplot.title('Global Agent Count Over Time')
        pyplot.legend()

        pyplot.show(block=False)

class AgentTypeCountTracker(Tracker):
    """Counts the number of agents at each timestep by type.

    Attributes:
        data (dict): The number of agents at each timestep, organized 
            by type entries in this dictionary.
    """
    def __init__(self):
        super().__init__()
        self.data = {}

    def __call__(self, simulation):
        """Tracks the number of agents in the simulation by type."""
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
        """Plots the data attribute using pyplot."""
        pyplot.style.use('ggplot')

        for agent_type, agent_type_count in self.data.items():
            typename = agent_type.__name__ + " Agent Count"
            line, = pyplot.plot(agent_type_count, label=typename)
            line.set_antialiased(True)

        pyplot.xlabel('Timestep')
        pyplot.ylabel('Agent Count')
        pyplot.title('Agent Count by Type Over Time')
        pyplot.legend()

        pyplot.show(block=False)