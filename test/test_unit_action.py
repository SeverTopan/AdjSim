import sys
import os
import pytest

from . import common

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_trivial():
    from adjsim import simulation, analysis, utility, decision

    action = lambda env, source: 0

    agent = simulation.Agent()
    agent.decision = decision.RandomSingleCastDecision()
    agent.actions["trivial"] = action

    test_sim = simulation.Simulation()
    test_sim.agents.add(agent)

    common.step_simulate_interpolation(test_sim)


def test_invalid_type():
    from adjsim import simulation, analysis, utility, decision

    action = True

    agent = simulation.Agent()
    agent.decision = decision.RandomSingleCastDecision()

    with pytest.raises(utility.InvalidActionException):
        agent.actions["trivial"] = action

def test_invalid_decision():
    from adjsim import simulation, analysis, utility

    action = lambda env, source: 0

    agent = simulation.Agent()
    agent.actions["trivial"] = action

    test_sim = simulation.Simulation()
    test_sim.agents.add(agent)

    with pytest.raises(utility.InvalidDecisionException):
        common.step_simulate_interpolation(test_sim)


def test_invalid_too_few_arguments():
    from adjsim import simulation, analysis, utility, decision

    action = lambda env: 0

    agent = simulation.Agent()
    agent.decision = decision.RandomSingleCastDecision()
    agent.actions["trivial"] = action

    test_sim = simulation.Simulation()
    test_sim.agents.add(agent)

    with pytest.raises(utility.InvalidActionException):
        common.step_simulate_interpolation(test_sim)

def test_invalid_too_many_arguments():
    from adjsim import simulation, analysis, utility, decision

    action = lambda env, source, kek: 0

    agent = simulation.Agent()
    agent.decision = decision.RandomSingleCastDecision()
    agent.actions["trivial"] = action

    test_sim = simulation.Simulation()
    test_sim.agents.add(agent)

    with pytest.raises(utility.InvalidActionException):
        common.step_simulate_interpolation(test_sim)


def test_timestep_count():
    from adjsim import simulation, analysis, decision

    def increment_action(env, source):
        source.count += 1  

    class TestAgent(simulation.Agent):
        def __init__(self):
            super().__init__()
            self.actions["increment"] = increment_action
            self.count = 0

    agent = TestAgent()
    agent.decision = decision.RandomSingleCastDecision()
    test_sim = simulation.Simulation()
    test_sim.agents.add(agent)

    common.step_simulate_interpolation(test_sim)

    assert agent.count == common.INTERPOLATION_NUM_TIMESTEP


    