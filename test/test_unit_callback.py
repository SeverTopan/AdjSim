import sys
import os
import pytest

import numpy as np

from . import common

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_agent_add():
    from adjsim import core, analysis, decision

    def addition_callback(agent):
        addition_callback.count += 1
    addition_callback.count = 0

    def increment_agents(env, source):
        env.agents.add(TestAgent()) 

    class TestAgent(core.Agent):
        def __init__(self):
            super().__init__()
            self.actions["increment"] = increment_agents
            self.decision = decision.RandomSingleCastDecision()

    test_sim = core.Simulation()
    test_sim.callbacks.agent_added.register(addition_callback)
    test_sim.agents.add(TestAgent())
    test_sim.trackers["count"] = analysis.AgentTypeCountTracker()
    
    common.step_simulate_interpolation(test_sim)

    assert addition_callback.count == 2**common.INTERPOLATION_NUM_TIMESTEP


def test_agent_remove():
    from adjsim import core, analysis, decision

    def removal_callback(agent):
        removal_callback.count += 1
    removal_callback.count = 0

    def decrement_agents(env, source):
        env.agents.remove(source)

    class TestAgent(core.Agent):
        def __init__(self):
            super().__init__()
            self.actions["decrement"] = decrement_agents
            self.decision = decision.RandomSingleCastDecision()

    test_sim = core.Simulation()
    test_sim.callbacks.agent_removed.register(removal_callback)
    for _ in range(20):
        test_sim.agents.add(TestAgent())

    common.step_simulate_interpolation(test_sim)

    assert removal_callback.count == 20

def test_agent_move():
    from adjsim import core, utility, decision

    def move_callback(agent):
        move_callback.count += 1
    move_callback.count = 0

    def move(env, source):
        source.x += 10
        source.y += 10

    class TestAgent(core.VisualAgent):
        def __init__(self, x, y):
            super().__init__(pos=np.array([x, y]))
            self.decision = decision.RandomSingleCastDecision()
            self.actions["move"] = move


    test_sim = core.Simulation()
    test_sim.callbacks.agent_moved.register(move_callback)
    test_sim.agents.add(TestAgent(0, 0))
    test_sim.agents.add(TestAgent(0, -10))

    common.step_simulate_interpolation(test_sim)

    assert move_callback.count == 4*common.INTERPOLATION_NUM_TIMESTEP # 2 agents * 2 updates per move


# test core ended 