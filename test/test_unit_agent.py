import sys
import os
import pytest

from . import common

def test_trivial():
    from adjsim import core, utility, decision

    class TrivialAgent(core.Agent):
        def __init__(self):
            super().__init__()
            self.decision = decision.RandomSingleCastDecision()

    class TrivialSpatialAgent(core.SpatialAgent):
        def __init__(self):
            super().__init__()
            self.decision = decision.RandomSingleCastDecision()

    class TrivialVisualAgent(core.VisualAgent):
        def __init__(self):
            super().__init__()
            self.decision = decision.RandomSingleCastDecision()

    test_sim = core.Simulation()
    test_sim.agents.add(TrivialAgent())
    test_sim.agents.add(TrivialSpatialAgent())
    test_sim.agents.add(TrivialVisualAgent())
    
    common.step_simulate_interpolation(test_sim)

def test_invalid_type():
    from adjsim import core, utility

    test_sim = core.Simulation()

    with pytest.raises(utility.InvalidAgentException):
        test_sim.agents.add({"I'm not valid!"})


def test_agent_add():
    from adjsim import core, analysis, decision

    def increment_agents(env, source):
        env.agents.add(TestAgent()) 

    class TestAgent(core.Agent):
        def __init__(self):
            super().__init__()
            self.actions["increment"] = increment_agents
            self.decision = decision.RandomSingleCastDecision()

    test_sim = core.Simulation()
    test_sim.agents.add(TestAgent())

    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.agents) == 2**common.INTERPOLATION_NUM_TIMESTEP

def test_agent_remove():
    from adjsim import core, analysis, decision

    def decrement_agents(env, source):
        env.agents.remove(source)

    class TestAgent(core.Agent):
        def __init__(self):
            super().__init__()
            self.actions["decrement"] = decrement_agents
            self.decision = decision.RandomSingleCastDecision()

    test_sim = core.Simulation()
    for _ in range(20):
        test_sim.agents.add(TestAgent())

    common.step_simulate_interpolation(test_sim)

    assert len(test_sim.agents) == 0