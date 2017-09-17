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


def test_simulation():
    from adjsim import simulation

    test_sim = simulation.Simulation()

    common.step_simulate_interpolation(test_sim)


def test_sandbox():
    from adjsim import simulation, analysis, utility

    test_sim = simulation.VisualSimulation()
    
    
    


    