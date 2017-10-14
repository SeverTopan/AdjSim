import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_tag():
    from demo import tag

    sim = tag.TaggerSimulation()
    sim._wait_on_visual_init = 0
    sim.start()
    sim.simulate(20)
    sim.end()

def test_bacteria():
    from demo import bacteria

    sim = bacteria.BacteriaSimulation()
    sim._wait_on_visual_init = 0
    sim.start()
    sim.simulate(20)
    sim.end()

def test_bacteria_intelligent():
    from demo import bacteria_qlearning

    sim = bacteria_qlearning.BacteriaTrainSimulation()
    sim.start()
    sim.simulate(10)
    sim.end()

    sim = bacteria_qlearning.BacteriaTestSimulation()
    sim.start()
    sim.simulate(10)
    sim.end()

def test_predator_prey():
    from demo import predator_prey

    sim = predator_prey.PredatorPreySimulation()
    sim._wait_on_visual_init = 0
    sim.start()
    sim.simulate(10)
    sim.end()

def test_jupiter_moon_system():
    from demo import jupiter_moon_system

    sim = jupiter_moon_system.JupiterMoonSystemSimulation()
    sim._wait_on_visual_init = 0
    sim.start()
    sim.simulate(10)
    sim.end()

def test_gol_gosper_glider_gun():
    from demo import gol_gosper_glider_gun

    sim = gol_gosper_glider_gun.GameOfLife()
    sim._wait_on_visual_init = 0
    sim.start()
    sim.simulate(10)
    sim.end()

def test_gol_block_laying_switch_engine():
    from demo import gol_block_laying_switch_engine

    sim = gol_block_laying_switch_engine.GameOfLife()
    sim._wait_on_visual_init = 0
    sim.start()
    sim.simulate(10)
    sim.end()
    