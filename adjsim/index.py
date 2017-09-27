
import numpy as np


class Index(object):
    pass

class GridIndex(Index):

    NEIGHBOUR_ITERATION_LIST = [[1,0], [1,1], [1,0], [1,-1], [-1,0], [-1,-1], [0,-1], [-1,1]]
    NEIGHBOUR_ITERATION_ARRAYS = [np.array(i) for i in NEIGHBOUR_ITERATION_LIST]

    def __init__(self, simulation):
        super().__init__()

        self.grid = {}

        # Initialize grid.
        for agent in simulation.agents:
            entry = self.grid.get(agent.pos)

            if entry is None:
                self.grid[np.floor(agent.pos)] = [agent]
            else:
                entry.append(agent)


    def get_neighbours(self, pos):
        if not type(pos) == np.ndarray or pos.shape != (2,):
            raise TypeError
        
        floored_pos = np.floor(pos)

        # Iterate through neighbour indices.
        for array in GridIndex.NEIGHBOUR_ITERATION_ARRAYS:
            neighbours = self.grid.get(floored_pos + array)
            if neighbours is not None:
                yield neighbours

    def update(self, simulation, agent):
        pass


