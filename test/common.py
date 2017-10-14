import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


INTERPOLATION_NUM_TIMESTEP = 9

def step_simulate_interpolation(simulation):
    simulation.start()
    simulation.step()
    simulation.simulate(3)
    simulation.step()
    simulation.simulate(3)
    simulation.step()
    simulation.end()
