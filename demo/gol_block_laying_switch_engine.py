"""Conway's Game of Life Simulation.

Implementation of Conway's Game of Life (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
"""

# Standard.
import random
import sys
import os

# Third party.
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from adjsim import core, utility, decision, analysis, color


# Constants.
CELL_SIZE = 5
INTIAL_COORDINATES = [(0,0),                          # 1st column
                    (2,0),(2,1),                    # 2nd column
                    (4,2),(4,3),(4,4),              # 3rd column
                    (6,3),(6,4),(6,5),(7,4)]        # 4th column


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
            if not simulation.indices.grid.get_inhabitants(coord):
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
        

class Cell(core.VisualAgent):
    def __init__(self, pos):
        super().__init__(pos=pos)
        self.size = 5

class Meta(core.Agent):
    def __init__(self):
        super().__init__()

        self.actions["compute"] = compute
        self.decision = decision.RandomSingleCastDecision()

class GameOfLife(core.VisualSimulation):
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
