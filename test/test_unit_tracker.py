import sys
import os
import pytest

from . import common

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_valid():
    from adjsim import simulation, analysis, utility

    class ValidTracker(analysis.Tracker):
        def __call__(self, value):
            pass

    test_sim = simulation.Simulation()
    test_sim.trackers["count"] = ValidTracker()

    common.step_simulate_interpolation(test_sim)


def test_invalid_too_many_arguments():
    from adjsim import simulation, analysis, utility

    class InvalidTracker(analysis.Tracker):
        def __call__(self, hello, bye):
            pass
    
    test_sim = simulation.Simulation()
    test_sim.trackers["count"] = InvalidTracker()

    with pytest.raises(utility.InvalidTrackerException):
        common.step_simulate_interpolation(test_sim)


def test_invalid_too_few_arguments():
    from adjsim import simulation, analysis, utility

    class InvalidTracker(analysis.Tracker):
        def __call__(self):
            pass
    
    test_sim = simulation.Simulation()
    test_sim.trackers["count"] = InvalidTracker()

    with pytest.raises(utility.InvalidTrackerException):
        common.step_simulate_interpolation(test_sim)

def test_invalid_data():
    from adjsim import simulation, analysis, utility

    class InvalidTracker(analysis.Tracker):
        def __init__(self):
            self.data = {}
        
        def __call__(self):
            pass

    test_sim = simulation.Simulation()
    test_sim.trackers["count"] = InvalidTracker()

    with pytest.raises(utility.InvalidTrackerException):
        common.step_simulate_interpolation(test_sim)


def test_invalid_type():
    from adjsim import simulation, analysis, utility

    test_sim = simulation.Simulation()

    with pytest.raises(utility.InvalidTrackerException):
        test_sim.trackers["count"] = lambda x: 0


def test_trivial_agent_count():
    from adjsim import simulation, analysis

    test_sim = simulation.Simulation()
    test_sim.trackers["count"] = analysis.AgentCountTracker()

    common.step_simulate_interpolation(test_sim)

    assert test_sim.trackers["count"].data == [0 for i in range(common.INTERPOLATION_NUM_TIMESTEP + 1)]

def test_exponential_agent_count():
    from adjsim import simulation, analysis, decision

    def increment_agents(env, source):
        env.agents.add(TestAgent()) 

    class TestAgent(simulation.Agent):
        def __init__(self):
            super().__init__()
            self.actions["increment"] = increment_agents
            self.decision = decision.RandomSingleCastDecision()

    test_sim = simulation.Simulation()
    test_sim.agents.add(TestAgent())
    test_sim.trackers["count"] = analysis.AgentCountTracker()
    

    common.step_simulate_interpolation(test_sim)

    assert test_sim.trackers["count"].data == [2**i for i in range(common.INTERPOLATION_NUM_TIMESTEP + 1)]

def test_exponential_agent_type_count():
    from adjsim import simulation, analysis, decision

    def increment_agents(env, source):
        env.agents.add(TestAgent()) 

    class TestAgent(simulation.Agent):
        def __init__(self):
            super().__init__()
            self.actions["increment"] = increment_agents
            self.decision = decision.RandomSingleCastDecision()

    test_sim = simulation.Simulation()
    test_sim.agents.add(TestAgent())
    test_sim.trackers["count"] = analysis.AgentTypeCountTracker()
    
    common.step_simulate_interpolation(test_sim)

    print(test_sim.trackers["count"].data)

    assert test_sim.trackers["count"].data[TestAgent] == [2**i for i in range(common.INTERPOLATION_NUM_TIMESTEP + 1)]


    