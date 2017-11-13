import pytest

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