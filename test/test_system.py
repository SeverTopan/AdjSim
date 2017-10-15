import sys
import os
import pytest

def test_tag():
    from examples.tag.simulation import TaggerSimulation

    sim = TaggerSimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(20)

def test_bacteria():
    from examples.bacteria.simulation import BasicBacteriaSimulation

    sim = BasicBacteriaSimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(20)

def test_bacteria_qlearning():
    from examples.bacteria.simulation import QLearningBacteriaTrainSimulation, QLearningBacteriaTestSimulation

    sim = QLearningBacteriaTrainSimulation()
    sim.simulate(10)

    sim = QLearningBacteriaTestSimulation()
    sim.simulate(10)

def test_predator_prey():
    from examples.predator_prey.simulation import PredatorPreySimulation

    sim = PredatorPreySimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(10)

def test_jupiter_moon_system():
    from examples.physics.simulation import JupiterMoonSystemSimulation

    sim = JupiterMoonSystemSimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(10)

def test_gol_gosper_glider_gun():
    from examples.game_of_life.simulation import GosperGliderGun

    sim = GosperGliderGun()
    sim._wait_on_visual_init = 0
    sim.simulate(10)

def test_gol_block_laying_switch_engine():
    from examples.game_of_life.simulation import BlockLayingSwitchEngine

    sim = BlockLayingSwitchEngine()
    sim._wait_on_visual_init = 0
    sim.simulate(10)
    