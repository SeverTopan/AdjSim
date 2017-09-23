import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_tag():
    from demo import tag

    sim = tag.TaggerSimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(20)

def test_bacteria():
    from demo import bacteria

    sim = bacteria.BacteriaSimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(20)

def test_predator_prey():
    from demo import predator_prey

    sim = predator_prey.PredatorPreySimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(10)
    