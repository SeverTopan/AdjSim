"""Conway's Game of Life Simulation.

Implementation of Conway's Game of Life (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
"""

# Standard.
import random
import sys
import os

# Third party.
import numpy as np
from adjsim import core, utility, decision, analysis, color


# Constants.
CELL_SIZE = 5

def compute(simulation, source):
    """Main game loop."""
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

class BlockLayingSwitchEngine(core.VisualSimulation):
    """Implementation of a block laying switch engine pattern starting condition.

    This is one of the smallest patterns to exhibit infinite growth in Conway's
    Game of Life. Description can be found at
    http://www.conwaylife.com/w/index.php?title=Block-laying_switch_engine.
    """

    INTIAL_COORDINATES = [
        (0,0),                          # 1st column
        (2,0),(2,1),                    # 2nd column
        (4,2),(4,3),(4,4),              # 3rd column
        (6,3),(6,4),(6,5),(7,4)         # 4th column
    ]

    def __init__(self):
        super().__init__()

        self.indices.grid.initialize(CELL_SIZE)
        
        self.agents.add(Meta())
        for coord in BlockLayingSwitchEngine.INTIAL_COORDINATES:
            self.agents.add(Cell(np.array(coord) * CELL_SIZE))

class GosperGliderGun(core.VisualSimulation):
    """Implementation of a gosper glider gun pattern starting condition.

    This was the first discovered pattern to exhibit infinite growth. It was
    a submission by Bill Gosper in response to a $50 contest to prove/disprove
    Conway's conjecture that there exist patterns that grow infinitely. 
    Description can be found at
    http://www.conwaylife.com/w/index.php?title=Gosper_glider_gun.
    """
    
    INTIAL_COORDINATES = [
        (0,0),(1,0),(1,1),(0,1),                                            # left-most block
        (10,0),(10,1),(10,-1),(11,2),(11,-2),(12,3),(12,-3),(13,3),(13,-3), # curve on left
        (14,0),(15,2),(15,-2),(16,1),(16,-1),(16,0),(17,0),                 # 'play button' on left
        (20,1),(20,2),(20,3),(21,1),(21,2),(21,3),(22,0),(22,4),            # 2x3 + 2 on right
        (24,-1),(24,0),(24,4),(24,5),                                       # trailing 'winglets' on right
        (34,2),(34,3),(35,2),(35,3)                                        # right-most block
    ]

    def __init__(self):
        super().__init__()

        self.indices.grid.initialize(CELL_SIZE)
        
        self.agents.add(Meta())
        for coord in GosperGliderGun.INTIAL_COORDINATES:
            self.agents.add(Cell(np.array(coord) * CELL_SIZE))
