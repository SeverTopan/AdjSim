import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def adjSim():
    import AdjSim
    adjSim = AdjSim.AdjSim(logInstance=False)

    AdjSim.Intelligence.QLearning.I_FILE_NAME = "none"

    adjSim.clearEnvironment()
    return adjSim

def test_bacteria(adjSim):
    from demo import bacteria
    bacteria.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=False)

def test_predator_prey(adjSim):
    from demo import predator_prey
    predator_prey.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=False)

def test_gosper_glider_gun(adjSim):
    from demo import gol_block_laying_switch_engine
    gol_block_laying_switch_engine.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=False)

def test_jupiter_moon_system(adjSim):
    from demo import jupiter_moon_system
    jupiter_moon_system.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=False)
    