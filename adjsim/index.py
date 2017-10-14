
import numpy as np

from . import core
from . import utility

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
        self._initialized = False
        

    def initialize(self, grid_size):
        self._grid_size = grid_size

        for agent in self._simulation.agents:
            # Only iterate over derived of SpatialAgent
            if not issubclass(type(agent), core.SpatialAgent):
                continue

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

        # Set flag.
        self._initialized = True

    def get_neighbour_coordinates(self, pos):
        # Check flag.
        if not self._initialized:
            raise utility.IndexInitializationException()
        
        # Check type.
        if type(pos) != np.ndarray or pos.shape != (2,):
            raise TypeError
        
        floored_pos = np.floor(pos/self._grid_size)*self._grid_size

        # Iterate through neighbour indices.
        return_list = []
        for array in GridIndex.NEIGHBOUR_ITERATION_ARRAYS:
            inquiry_array = floored_pos + array*self._grid_size
            return_list.append(inquiry_array)

        return return_list

    def _get_inhabitants_list(self, pos):
        # Iterate through pos indices.
        return_list = []
        for array in pos:
            if type(array) != np.ndarray or array.shape != (2,):
                raise TypeError

            found = self._get_inhabitants_single(array)
            if not found is None:
                return_list += found

        return return_list

    def _get_inhabitants_single(self, pos):
        if type(pos) != np.ndarray or pos.shape != (2,):
                raise TypeError
        
        found = self._grid.get((pos[0], pos[1]))
        if found is None:
            return list()
        else:
            return list(found)

    def get_inhabitants(self, pos):
        # Check flag.
        if not self._initialized:
            raise utility.IndexInitializationException()
        
        # Check if input is iterable and NOT a single ndarray (which happens to also be iterable).
        try:
            iter(pos)
            if type(pos) == np.ndarray:
                raise TypeError
        except TypeError:
           return self._get_inhabitants_single(pos)
        else:
            return self._get_inhabitants_list(pos)


    def get_neighbours(self, pos):
        # Check flag.
        if not self._initialized:
            raise utility.IndexInitializationException()
        
        # Check type.
        if type(pos) != np.ndarray or pos.shape != (2,):
            raise TypeError
        
        return self.get_inhabitants(self.get_neighbour_coordinates(pos))


    def _update(self, agent):
        # We only care if the agent is spatial.
        if not issubclass(type(agent), core.SpatialAgent):
            return

        inquiry_array = self._agent_mapping.get(agent)
        new_array = np.floor(agent.pos/self._grid_size)*self._grid_size

        # Check if entry exists.
        if not inquiry_array is None:

            # Remove previous agent reference.
            # If last entry, remove from dictionary.
            target_agents = self._grid.get((inquiry_array[0], inquiry_array[1]))
            if len(target_agents) == 1:
                del self._grid[(inquiry_array[0], inquiry_array[1])]
            else:
                target_agents.remove(agent)


        # Add new coordinates if not a deletion.
        if agent._exists:
            entry = self._grid.get((new_array[0], new_array[1]))

            if entry is None:
                self._grid[(new_array[0], new_array[1])] = {agent}
            else:
                entry.add(agent)

            self._agent_mapping[agent] = new_array


