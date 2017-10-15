import sys
import os
import pytest

from . import common

def test_trivial():
    from adjsim import core, analysis, utility, decision

    action = lambda env, source: 0

    agent = core.Agent()
    agent.decision = decision.RandomSingleCastDecision()
    agent.actions["trivial"] = action

    test_sim = core.Simulation()
    test_sim.agents.add(agent)

    common.step_simulate_interpolation(test_sim)


def test_invalid_type():
    from adjsim import core, analysis, utility, decision

    action = True

    agent = core.Agent()
    agent.decision = decision.RandomSingleCastDecision()

    with pytest.raises(utility.ActionException):
        agent.actions["trivial"] = action

def test_invalid_decision():
    from adjsim import core, analysis, utility

    action = lambda env, source: 0

    agent = core.Agent()
    agent.decision = None
    agent.actions["trivial"] = action

    test_sim = core.Simulation()
    test_sim.agents.add(agent)

    with pytest.raises(utility.DecisionException):
        common.step_simulate_interpolation(test_sim)


def test_invalid_too_few_arguments():
    from adjsim import core, analysis, utility, decision

    action = lambda env: 0

    agent = core.Agent()
    agent.decision = decision.RandomSingleCastDecision()
    agent.actions["trivial"] = action

    test_sim = core.Simulation()
    test_sim.agents.add(agent)

    with pytest.raises(utility.DecisionException):
        common.step_simulate_interpolation(test_sim)

def test_invalid_too_many_arguments():
    from adjsim import core, analysis, utility, decision

    action = lambda env, source, kek: 0

    agent = core.Agent()
    agent.decision = decision.RandomSingleCastDecision()
    agent.actions["trivial"] = action

    test_sim = core.Simulation()
    test_sim.agents.add(agent)

    with pytest.raises(utility.DecisionException):
        common.step_simulate_interpolation(test_sim)


def test_timestep_count():
    from adjsim import core, analysis, decision

    def increment_action(env, source):
        source.count += 1  

    class TestAgent(core.Agent):
        def __init__(self):
            super().__init__()
            self.actions["increment"] = increment_action
            self.count = 0

    agent = TestAgent()
    agent.decision = decision.RandomSingleCastDecision()
    test_sim = core.Simulation()
    test_sim.agents.add(agent)

    common.step_simulate_interpolation(test_sim)

    assert agent.count == common.INTERPOLATION_NUM_TIMESTEP


    