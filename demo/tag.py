"""
    
"""
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from adjsim import simulation, utility, decision

from PyQt5 import QtGui

ARENA_BOUND = 100
TAG_DIST_SQUARE = 100
MOVE_DIST = 20

def move(simulation, source):
    movement = (np.random.rand(2) - 0.5) * MOVE_DIST
    source.pos = np.clip(source.pos + movement, -ARENA_BOUND, ARENA_BOUND)
    source.step_complete = True

def tag(simulation, source):  

    if not source.is_it:
        return

    closest_distance = sys.float_info.max
    nearest_neighbour = None
    for agent in simulation.agents:
        if agent.id == source.id:
            continue

        distance = utility.distance_square(agent, source)
        if distance < closest_distance:
            nearest_neighbour = agent
            closest_distance = distance

    if closest_distance > TAG_DIST_SQUARE:
        return


    assert nearest_neighbour

    nearest_neighbour.is_it = True
    nearest_neighbour.color = QtGui.QColor(utility.RED_DARK)
    nearest_neighbour.order = 1
    source.is_it = False
    source.order = 0
    source.color = QtGui.QColor(utility.BLUE_DARK)

class Tagger(simulation.VisualAgent):

    def __init__(self, x, y, is_it):
        super().__init__()

        self.is_it = is_it
        self.color = QtGui.QColor(utility.RED_DARK) if is_it else QtGui.QColor(utility.BLUE_DARK)
        self.pos = np.array([x, y])
        self.decision = decision.RandomSingleCastDecision()

        self.actions["move"] = move
        self.actions["tag"] = tag

        if is_it:
            self.order = 1


class TaggerSimulation(simulation.VisualSimulation):

    def __init__(self):
        super().__init__()

        for i in range(5):
            for j in range(5):
                self.agents.add(Tagger(20*i, 20*j, False))

        self.agents.add(Tagger(-10, -10, True))


if __name__ == "__main__":
    sim = TaggerSimulation()
    sim.simulate(100)   
