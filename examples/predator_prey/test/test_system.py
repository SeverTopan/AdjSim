import pytest

def test_predator_prey():
    from examples.predator_prey.simulation import PredatorPreySimulation

    sim = PredatorPreySimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(10)