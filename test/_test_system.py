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

def test_logging(adjSim):
    import AdjSim
    adjSim = AdjSim.AdjSim(logInstance=True)

def test_bacteria(adjSim):
    from demo import bacteria
    bacteria.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=False)

def test_bacteria_graphics(adjSim):
    from demo import bacteria
    bacteria.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=True, plotIndices=False)

def test_bacteria_plot(adjSim):
    from demo import bacteria
    import AdjSim
    from matplotlib import pyplot

    pyplot.ion()
    bacteria.generateEnv(adjSim.environment)
    adjSim.environment.indices.add(AdjSim.Analysis.Index(adjSim.environment, AdjSim.Simulation.Analysis.Index.ACCUMULATE_AGENTS, 'type'))
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=True)

def test_bacteria_intelligent(adjSim):
    from demo import bacteria_intelligent
    import AdjSim

    AdjSim.Intelligence.QLearning.setIOFileName("bacteria_intelligent_demo.qlearning.pkl")

    bacteria_intelligent.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=False, simulationType=AdjSim.TRAIN)

    # simulate a second time to use previously generated intelligence file
    adjSim.clearEnvironment()
    bacteria_intelligent.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=False, simulationType=AdjSim.TRAIN)

    # simulate a third time to test simulation efficacy
    adjSim.clearEnvironment()
    bacteria_intelligent.generateEnv(adjSim.environment)
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=False, simulationType=AdjSim.TEST)

def test_bacteria_intelligent_plot(adjSim):
    from demo import bacteria_intelligent
    import AdjSim
    from matplotlib import pyplot

    AdjSim.Intelligence.QLearning.setIOFileName("bacteria_intelligent_demo.qlearning.pkl")

    pyplot.ion()
    bacteria_intelligent.generateEnv(adjSim.environment)
    adjSim.environment.indices.add(AdjSim.Analysis.Index(adjSim.environment, AdjSim.Simulation.Analysis.Index.AVERAGE_QLEARNING_REWARD))
    adjSim.environment.indices.add(AdjSim.Analysis.Index(adjSim.environment, AdjSim.Simulation.Analysis.Index.INDIVIDUAL_QLEARNING_REWARD))
    adjSim.environment.indices.add(AdjSim.Analysis.Index(adjSim.environment, AdjSim.Simulation.Analysis.Index.AVERAGE_GOAL_VALUES))
    adjSim.environment.indices.add(AdjSim.Analysis.Index(adjSim.environment, AdjSim.Simulation.Analysis.Index.INDIVIDUAL_GOAL_VALUES))
    adjSim.environment.indices.add(AdjSim.Analysis.Index(adjSim.environment, AdjSim.Simulation.Analysis.Index.ACCUMULATE_AGENTS, 'type'))
    adjSim.simulate(10, graphicsEnabled=False, plotIndices=True, simulationType=AdjSim.TRAIN)
    
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
    