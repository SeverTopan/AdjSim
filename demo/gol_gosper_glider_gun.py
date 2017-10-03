
# standard
import random
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# third party
from PyQt5 import QtGui, QtCore
import numpy as np
from adjsim import simulation, utility, decision, analysis, color


# CONSTANTS
CELL_SIZE = 5
INTIAL_COORDINATES = [(0,0),(1,0),(1,1),(0,1),                                            # left-most block
                    (10,0),(10,1),(10,-1),(11,2),(11,-2),(12,3),(12,-3),(13,3),(13,-3), # curve on left
                    (14,0),(15,2),(15,-2),(16,1),(16,-1),(16,0),(17,0),                 # 'play button' on left
                    (20,1),(20,2),(20,3),(21,1),(21,2),(21,3),(22,0),(22,4),            # 2x3 + 2 on right
                    (24,-1),(24,0),(24,4),(24,5),                                       # trailing 'winglets' on right
                    (34,2),(34,3),(35,2),(35,3)]                                        # right-most block

INTIAL_COORDINATES_ = [(0,0), (0,1), (0,-1)]


def compute(simulation, source):

    # Track neighbours.
    global_empty_neighbours = set()
    kill_list = []
    birth_list = []
    for agent in simulation.agents:
        if agent == source:
            continue

        # Add coordinates to global empty list.
        neighbour_coords = simulation.indices.grid.get_neighbour_coordinates(agent.pos)
        for coord in neighbour_coords:
            if simulation.indices.grid.get_inhabitants(coord) is None:
                global_empty_neighbours.add((coord[0], coord[1]))

        # Count local neighbours.
        neighbours = simulation.indices.grid.get_neighbours(agent.pos)
        
        # Mark existing cells if needed (can't kill in set iteration). 
        if len(neighbours) < 2 or len(neighbours) > 3:
            kill_list.append(agent)


    # Mark new cells for birth if needed.
    for coord in global_empty_neighbours:
        array = np.array(coord)
        neighbours = simulation.indices.grid.get_neighbours(array)

        if len(neighbours) == 3:
            birth_list.append(array)

    # Kill agents.
    for agent in kill_list:
        simulation.agents.remove(agent)

    # Birth agents.
    for array in birth_list:
        simulation.agents.add(Cell(array))
        

class Cell(simulation.VisualAgent):
    def __init__(self, pos):
        super().__init__(pos=pos)
        self.size = 5

class Meta(simulation.Agent):
    def __init__(self):
        super().__init__()

        self.actions["compute"] = compute
        self.decision = decision.RandomSingleCastDecision()

class GameOfLife(simulation.VisualSimulation):
    def __init__(self):
        super().__init__()

        self.indices.grid.initialize(CELL_SIZE)
        
        self.agents.add(Meta())
        for coord in INTIAL_COORDINATES:
            self.agents.add(Cell(np.array(coord) * CELL_SIZE))


# MAIN FUNCTION
if __name__ == "__main__":
    sim = GameOfLife()
    sim.simulate(100)
