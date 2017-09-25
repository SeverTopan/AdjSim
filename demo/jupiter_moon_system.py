
# IMPORTS
# standard
import random
import sys
import os

# third party
from PyQt5 import QtGui, QtCore
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from adjsim import decision, simulation, utility

# CONSTANTS
GRAV_CONSTANT = 6.674e-11
TIMESTEP_LENGTH = 10000
DISTANCE_MULTIPLIER = 10000000


def gravity(simulation, source):
    # We need an ordering guarantee in the set traversal, so we list it.
    agent_list = list(simulation.agents)

    # Reset acceleration.
    for agent in agent_list:
        if agent == source:
            agent_list.remove(agent)
            continue

        agent.acc = np.array([0., 0.])

    # Calculate new accelleration.
    for source_agent in agent_list:
        for target_agent in agent_list:
            if source_agent == target_agent:
                break

            dist = (source_agent.pos - target_agent.pos) * DISTANCE_MULTIPLIER
            abs_dist_sq = np.sum(dist**2)
            abs_dist = abs_dist_sq**0.5
            abs_acc_target = source_agent.mass * GRAV_CONSTANT / abs_dist_sq
            abs_acc_source = target_agent.mass * GRAV_CONSTANT / abs_dist_sq

            target_agent.acc += abs_acc_target * dist / abs_dist
            source_agent.acc += -abs_acc_source * dist / abs_dist

    # Calculate velocity and position
    for agent in agent_list:
        agent.vel += agent.acc*TIMESTEP_LENGTH
        agent.pos += agent.vel*TIMESTEP_LENGTH/DISTANCE_MULTIPLIER

    source.step_complete = True


class Jupiter(simulation.VisualAgent):
    def __init__(self):
        super().__init__()
        self.vel = np.array([0., 0.])
        self.pos = np.array([0., 0.])
        self.acc = np.array([0., 0.])
        self.mass = 1.898e27
        self.size = 10
        self.color = QtGui.QColor(utility.ORANGE)

class Io(simulation.VisualAgent):
    def __init__(self):
        super().__init__()
        self.vel = np.array([0., 17.38e3])
        self.pos = np.array([42., 0.])
        self.acc = np.array([0., 0.])
        self.mass = 8.9e22
        self.size = 3
        self.color = QtGui.QColor(utility.GREY)

class Europa(simulation.VisualAgent):
    def __init__(self):
        super().__init__()
        self.vel = np.array([0., 13.7e3])
        self.pos = np.array([67., 0.])
        self.acc = np.array([0., 0.])
        self.mass = 4.8e22
        self.size = 3
        self.color = QtGui.QColor(utility.BLUE_LIGHT)

class Ganymede(simulation.VisualAgent):
    def __init__(self):
        super().__init__()
        self.vel = np.array([0., 10.88e3])
        self.pos = np.array([107., 0.])
        self.acc = np.array([0., 0.])
        self.mass = 1.48e23
        self.size = 5
        self.color = QtGui.QColor(utility.RED_DARK)

class Callisto(simulation.VisualAgent):
    def __init__(self):
        super().__init__()
        self.vel = np.array([0., 8.21e3])
        self.pos = np.array([188., 0.])
        self.acc = np.array([0., 0.])
        self.mass = 1.08e23
        self.size = 4
        self.color = QtGui.QColor(utility.BROWN_LIGHT)

class Physics(simulation.Agent):
    def __init__(self):
        super().__init__()
        self.actions["gravity"] = gravity
        self.decision = decision.RandomSingleCastDecision()

class JupiterMoonSystemSimulation(simulation.VisualSimulation):
    def __init__(self):
        super().__init__()
        self.agents.add(Physics())
        self.agents.add(Jupiter())
        self.agents.add(Io())
        self.agents.add(Europa())
        self.agents.add(Ganymede())
        self.agents.add(Callisto())

# MAIN FUNCTION
if __name__ == "__main__":
    sim = JupiterMoonSystemSimulation()
    sim.simulate(100)
