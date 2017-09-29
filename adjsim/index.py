
import numpy as np


class Index(object):
    pass

class GridIndex(Index):

    NEIGHBOUR_ITERATION_LIST = [[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]]
    NEIGHBOUR_ITERATION_ARRAYS = [np.array(i) for i in NEIGHBOUR_ITERATION_LIST]

    def __init__(self, simulation):
        super().__init__()

        self._grid = {}
        self._agent_mapping = {}
        self._simulation = simulation
        self._grid_size = 1
        

    def initialize(self, grid_size):
        self._grid_size = grid_size

        for agent in self._simulation.agents:
            inquiry_array = np.floor(agent.pos/grid_size)*grid_size
            entry = self._grid.get((inquiry_array[0], inquiry_array[1]))

            if entry is None:
                self._grid[(inquiry_array[0], inquiry_array[1])] = {agent}
            else:
                entry.add(agent)

            self._agent_mapping[agent] = inquiry_array

        # Init callbacks.
        self._simulation.callbacks.agent_added.register(self._update)
        self._simulation.callbacks.agent_moved.register(self._update)
        self._simulation.callbacks.agent_removed.register(self._update)


    def get_neighbours(self, pos):
        if type(pos) != np.ndarray or pos.shape != (2,):
            raise TypeError
        
        floored_pos = np.floor(pos/self._grid_size)*self._grid_size

        # Iterate through neighbour indices.
        return_list = []
        for array in GridIndex.NEIGHBOUR_ITERATION_ARRAYS:
            inquiry_array = floored_pos + array*self._grid_size
            neighbours = self._grid.get((inquiry_array[0], inquiry_array[1]))

            if neighbours is not None:
                for neighbour in neighbours:
                    return_list.append(neighbour)

        return return_list

    def _update(self, agent):
        inquiry_array = self._agent_mapping.get(agent)
        new_array = np.floor(agent.pos/self._grid_size)*self._grid_size

        # Check if entry exists.
        if not inquiry_array is None:

            # remove previous agent reference.
            self._grid.get((inquiry_array[0], inquiry_array[1])).remove(agent)


        # Add new coordinates if not a deletion.
        if agent._exists:
            entry = self._grid.get((new_array[0], new_array[1]))

            if entry is None:
                self._grid[(new_array[0], new_array[1])] = {agent}
            else:
                entry.add(agent)

            self._agent_mapping[agent] = new_array


