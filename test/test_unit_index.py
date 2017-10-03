import sys
import os
import pytest

import numpy as np

from . import common

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_grid_trivial(grid_size):
    from adjsim import simulation, analysis, decision

    class TestAgent(simulation.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = simulation.Simulation()

    test_sim.agents.add(TestAgent(np.array([0,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([0,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([2,0])*grid_size))

    test_sim.indices.grid.initialize(grid_size)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2
    
    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_grid_add_agent(grid_size):
    from adjsim import simulation, analysis, decision

    class TestAgent(simulation.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = simulation.Simulation()

    test_sim.indices.grid.initialize(grid_size)
    test_sim.agents.add(TestAgent(np.array([0,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([0,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([2,0])*grid_size))

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2
    
    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_grid_remove(grid_size):
    from adjsim import simulation, analysis, decision

    class TestAgent(simulation.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = simulation.Simulation()

    test_sim.agents.add(TestAgent(np.array([0,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([0,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([2,0])*grid_size))

    agent_to_remove = TestAgent(np.array([-1,0])*grid_size)
    test_sim.agents.add(agent_to_remove)

    test_sim.indices.grid.initialize(grid_size)

    test_sim.agents.remove(agent_to_remove)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2
    
    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_grid_move(grid_size):
    from adjsim import simulation, analysis, decision

    def move(simulation, source):
        source.y += grid_size

    class TestAgent(simulation.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)
            self.decision = decision.RandomSingleCastDecision()
            self.actions["move"] = move

    test_sim = simulation.Simulation()

    test_sim.agents.add(TestAgent(np.array([0,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([2,0])*grid_size))

    test_sim.indices.grid.initialize(grid_size)


    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2
    assert len(test_sim.indices.grid.get_neighbours(np.array([0,1])*grid_size)) == 3
    assert len(test_sim.indices.grid.get_neighbours(np.array([0,2])*grid_size)) == 1

    test_sim.step()

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2
    assert len(test_sim.indices.grid.get_neighbours(np.array([0,1])*grid_size)) == 2
    assert len(test_sim.indices.grid.get_neighbours(np.array([0,2])*grid_size)) == 3

    test_sim.step()

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 0
    assert len(test_sim.indices.grid.get_neighbours(np.array([0,1])*grid_size)) == 2
    assert len(test_sim.indices.grid.get_neighbours(np.array([0,2])*grid_size)) == 2


# get inhabitants single
# get inhabitants multiple ppl in one place
# get inhabitants wrong types
# call method before intialization
# agents with no coords
# removing a agent from a set returns back None, not an empty set