import pytest

def test_tag():
    from examples.tag.simulation import TaggerSimulation

    sim = TaggerSimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(20)