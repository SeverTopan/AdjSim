import sys
import os
import pytest

from . import common

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_trivial():
    from adjsim import simulation, utility, decision

    class TrivialAgent(simulation.Agent):
        def __init__(self):
            super().__init__()
            self.decision = decision.RandomSingleCastDecision()

    class TrivialSpatialAgent(simulation.SpatialAgent):
        def __init__(self):
            super().__init__()
            self.decision = decision.RandomSingleCastDecision()

    class TrivialVisualAgent(simulation.VisualAgent):
        def __init__(self):
            super().__init__()
            self.decision = decision.RandomSingleCastDecision()

    test_sim = simulation.Simulation()
    test_sim.agents.add(TrivialAgent())
    test_sim.agents.add(TrivialSpatialAgent())
    test_sim.agents.add(TrivialVisualAgent())

    common.step_simulate_interpolation(test_sim)

def test_invalid_type():
    from adjsim import simulation, utility

    test_sim = simulation.Simulation()

    with pytest.raises(utility.InvalidAgentException):
        test_sim.agents.add({"I'm not valid!"})


def test_agent_add():
    from adjsim import simulation, analysis, decision

    def increment_agents(env, source):
        env.agents.add(TestAgent()) 

    class TestAgent(simulation.Agent):
        def __init__(self):
            super().__init__()
            self.actions["increment"] = increment_agents
            self.count = 0
            self.decision = decision.RandomSingleCastDecision()

    test_sim = simulation.Simulation()
    test_sim.agents.add(TestAgent())

    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.agents) == 2**common.INTERPOLATION_NUM_TIMESTEP

def test_agent_remove():
    from adjsim import simulation, analysis, decision

    def increment_agents(env, source):
        env.agents.remove(source)

    class TestAgent(simulation.Agent):
        def __init__(self):
            super().__init__()
            self.actions["increment"] = increment_agents
            self.count = 0
            self.decision = decision.RandomSingleCastDecision()

    test_sim = simulation.Simulation()
    test_sim.agents.add(TestAgent())

    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.agents) == 0