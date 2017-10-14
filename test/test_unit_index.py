import sys
import os
import pytest

import numpy as np

from . import common

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_grid_uninitialized():
    from adjsim import core, analysis, decision, utility

    test_sim = core.Simulation()

    with pytest.raises(utility.IndexInitializationException):
        test_sim.indices.grid.get_inhabitants(np.array([0,0]))

    with pytest.raises(utility.IndexInitializationException):
        test_sim.indices.grid.get_neighbour_coordinates(np.array([0,0]))

    with pytest.raises(utility.IndexInitializationException):
        test_sim.indices.grid.get_neighbours(np.array([0,0]))

def test_grid_invalid_type():
    from adjsim import core, analysis, decision, utility

    test_sim = core.Simulation()
    test_sim.indices.grid.initialize(1)

    invalid_types = [(0,0), 5, object, [0,0], {0 : 0}]

    for invalid_type in invalid_types:
        with pytest.raises(TypeError):
            test_sim.indices.grid.get_inhabitants(invalid_type)
        with pytest.raises(TypeError):
            test_sim.indices.grid.get_neighbour_coordinates(invalid_type)
        with pytest.raises(TypeError):
            test_sim.indices.grid.get_neighbours(invalid_type)

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_inhabitants_single(grid_size):
    from adjsim import core, analysis, decision

    class TestAgent(core.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = core.Simulation()

    agent_00 = TestAgent(np.array([0,0])*grid_size)
    test_sim.agents.add(agent_00)
    agent_01 = TestAgent(np.array([0,1])*grid_size)
    test_sim.agents.add(agent_01)

    test_sim.indices.grid.initialize(grid_size)

    assert test_sim.indices.grid.get_inhabitants(np.array([0,0])*grid_size) == [agent_00]
    assert test_sim.indices.grid.get_inhabitants(np.array([0,1])*grid_size) == [agent_01]
    assert test_sim.indices.grid.get_inhabitants(np.array([1,1])*grid_size) == []

    common.step_simulate_interpolation(test_sim)

    assert test_sim.indices.grid.get_inhabitants(np.array([0,0])*grid_size) == [agent_00]
    assert test_sim.indices.grid.get_inhabitants(np.array([0,1])*grid_size) == [agent_01]
    assert test_sim.indices.grid.get_inhabitants(np.array([1,1])*grid_size) == []

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_inhabitants_multiple(grid_size):
    from adjsim import core, analysis, decision

    class TestAgent(core.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = core.Simulation()

    agent_00_1 = TestAgent(np.array([0,0])*grid_size)
    test_sim.agents.add(agent_00_1)
    agent_00_2 = TestAgent(np.array([0,0])*grid_size)
    test_sim.agents.add(agent_00_2)
    agent_01 = TestAgent(np.array([0,1])*grid_size)
    test_sim.agents.add(agent_01)

    test_sim.indices.grid.initialize(grid_size)

    found_00 = test_sim.indices.grid.get_inhabitants(np.array([0,0])*grid_size)
    assert found_00 == [agent_00_1, agent_00_2] or found_00 == [agent_00_2, agent_00_1]
    assert test_sim.indices.grid.get_inhabitants(np.array([0,1])*grid_size) == [agent_01]
    assert test_sim.indices.grid.get_inhabitants(np.array([1,1])*grid_size) == []

    common.step_simulate_interpolation(test_sim)

    found_00 = test_sim.indices.grid.get_inhabitants(np.array([0,0])*grid_size)
    assert found_00 == [agent_00_1, agent_00_2] or found_00 == [agent_00_2, agent_00_1]
    assert test_sim.indices.grid.get_inhabitants(np.array([0,1])*grid_size) == [agent_01]
    assert test_sim.indices.grid.get_inhabitants(np.array([1,1])*grid_size) == []

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_neighbours_trivial(grid_size):
    from adjsim import core, analysis, decision

    class TestAgent(core.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = core.Simulation()

    test_sim.agents.add(TestAgent(np.array([0,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([0,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([2,0])*grid_size))

    test_sim.indices.grid.initialize(grid_size)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2
    
    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_neighbours_trivial_no_coords(grid_size):
    from adjsim import core, analysis, decision

    class TestAgent(core.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    class DummyAgent(core.Agent):
        def __init__(self):
            super().__init__()

    test_sim = core.Simulation()

    test_sim.agents.add(TestAgent(np.array([0,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([0,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([2,0])*grid_size))

    test_sim.indices.grid.initialize(grid_size)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2
    
    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 2


@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_neighbours_trivial_multiple_inhabitants(grid_size):
    from adjsim import core, analysis, decision

    class TestAgent(core.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = core.Simulation()

    test_sim.agents.add(TestAgent(np.array([0,0])*grid_size))

    test_sim.agents.add(TestAgent(np.array([0,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([0,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([0,1])*grid_size))

    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))

    test_sim.agents.add(TestAgent(np.array([2,0])*grid_size))

    test_sim.indices.grid.initialize(grid_size)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 5
    
    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.indices.grid.get_neighbours(np.array([0,0])*grid_size)) == 5

@pytest.mark.parametrize("grid_size", [1, 5, 7, 12, 17])
def test_grid_add_agent(grid_size):
    from adjsim import core, analysis, decision

    class TestAgent(core.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = core.Simulation()

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
    from adjsim import core, analysis, decision

    class TestAgent(core.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)

    test_sim = core.Simulation()

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
    from adjsim import core, analysis, decision

    def move(simulation, source):
        source.y += grid_size

    class TestAgent(core.SpatialAgent):
        def __init__(self, pos):
            super().__init__(pos=pos)
            self.decision = decision.RandomSingleCastDecision()
            self.actions["move"] = move

    test_sim = core.Simulation()

    test_sim.agents.add(TestAgent(np.array([0,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,0])*grid_size))
    test_sim.agents.add(TestAgent(np.array([1,1])*grid_size))
    test_sim.agents.add(TestAgent(np.array([2,0])*grid_size))

    test_sim.indices.grid.initialize(grid_size)
    test_sim.start()

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

    test_sim.end()
