import sys
import os
import pytest

from . import common

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def step_simulate_interpolation(simulation):
    simulation.step()
    simulation.simulate(3)
    simulation.step()
    simulation.simulate(3)
    simulation.step()


def test_trivial():
    from adjsim import simulation

    test_sim = simulation.Simulation()

    common.step_simulate_interpolation(test_sim)

    assert test_sim.time == common.INTERPOLATION_NUM_TIMESTEP

def test_valid_end_condition():
    from adjsim import simulation

    test_sim = simulation.Simulation()
    test_sim.end_condition = lambda env: env.time == common.INTERPOLATION_NUM_TIMESTEP - 1

    common.step_simulate_interpolation(test_sim)

    assert test_sim.time == common.INTERPOLATION_NUM_TIMESTEP

def test_invalid_end_condition():
    from adjsim import simulation, utility

    test_sim = simulation.Simulation()
    test_sim.end_condition = True

    with pytest.raises(utility.InvalidEndConditionException):
        common.step_simulate_interpolation(test_sim)



def test_sandbox():
    from adjsim import simulation, analysis, utility

    test_sim = simulation.VisualSimulation()
    
    
    


    