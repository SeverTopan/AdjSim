"""
    
"""
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from adjsim import simulation, utility

from PyQt5 import QtGui

ARENA_BOUND = 100
TAG_DIST = 10
MOVE_DIST = 20

def move(environment, source_agent):
    movement = (np.random.rand(2) - 0.5) * MOVE_DIST
    source_agent.pos = np.clip(source_agent.pos + movement, -ARENA_BOUND, ARENA_BOUND)

def tag(environment, source_agent):  

    if not source_agent.is_it:
        return

    closest_distance = sys.float_info.max
    nearest_neighbour = None
    for agent in environment.agents:
        if agent.id == source_agent.id:
            continue

        distance = utility.distance(agent, source_agent)
        if distance < closest_distance:
            nearest_neighbour = agent
            closest_distance = distance

    # if closest_distance > TAG_DIST:
    #     return


    assert nearest_neighbour

    nearest_neighbour.is_it = True
    nearest_neighbour.color = QtGui.QColor(utility.RED_DARK)
    nearest_neighbour.order = 1
    source_agent.is_it = False
    source_agent.order = 0
    source_agent.color = QtGui.QColor(utility.BLUE_DARK)

    print("post cast:", nearest_neighbour, source_agent)

    for agent in environment.agents:
        print("agent", agent, agent.is_it)



class Tagger(simulation.VisualAgent):

    def __init__(self, x, y, is_it):
        super().__init__()

        self.is_it = is_it
        self.color = QtGui.QColor(utility.RED_DARK) if is_it else QtGui.QColor(utility.BLUE_DARK)
        self.pos = np.array([x, y])

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
