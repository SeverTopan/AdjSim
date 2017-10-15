import sys
import os
import pytest

INTERPOLATION_NUM_TIMESTEP = 9

def step_simulate_interpolation(simulation):
    simulation.start()
    simulation.step()
    simulation.step(3)
    simulation.step()
    simulation.step(3)
    simulation.step()
    simulation.end()
