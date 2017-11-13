import pytest

def test_jupiter_moon_system():
    from examples.orbital.simulation import JupiterMoonSystemSimulation

    sim = JupiterMoonSystemSimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(10)