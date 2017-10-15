import sys
import os
import pytest

import numpy as np

from . import common

@pytest.mark.parametrize("mutable_min,mutable_max", [(0, 1), (0, 7), (-7, 0),(300, 400) ])
def test_qlearning_basic(mutable_min, mutable_max):
    from adjsim import core, utility, decision

    def move(env, source):
        move.count += 1
        source.step_complete = True
    move.count = 0

    def perception(env, source):
        perception.count += 1
        return 1
    perception.count = 0

    def loss(env, source):
        loss.count += 1
        return 1
    loss.count = 0

    class TestAgent(core.VisualAgent):
        def __init__(self, x, y, sim):
            super().__init__(pos=np.array([x, y]))

            self.decision = decision.QLearningDecision(perception=perception, loss=loss, 
                callbacks=sim.callbacks, output_file_name=None, input_file_name=None)

            self.actions["move"] = move

            self.mutable = decision.DecisionMutableFloat(mutable_min, mutable_max)


    test_sim = core.Simulation()
    agent = TestAgent(0, 0, test_sim)
    test_sim.agents.add(agent)

    test_sim.simulate(1)

    # Check proper call counts.
    assert move.count == 1
    assert perception.count == 1
    assert loss.count == 1

    # Check expected q_table entries.
    assert agent.decision.q_table[1].loss == 1
    assert len(agent.decision.q_table[1].action_premise.iterations) == 1
    assert len(agent.decision.q_table[1].action_premise.iterations[0].decision_mutables) == 1
    
    decision_mutable_premise = agent.decision.q_table[1].action_premise.iterations[0].decision_mutables[0]
    assert decision_mutable_premise.name == "mutable"
    assert decision_mutable_premise.value < mutable_max and decision_mutable_premise.value > mutable_min
    assert agent.decision.q_table[1].action_premise.iterations[0].action_name == "move"


    