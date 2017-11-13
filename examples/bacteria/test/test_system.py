import pytest

def test_bacteria():
    from examples.bacteria.simulation import BasicBacteriaSimulation

    sim = BasicBacteriaSimulation()
    sim._wait_on_visual_init = 0
    sim.simulate(20)

def test_bacteria_qlearning():
    from examples.bacteria.simulation import QLearningBacteriaTrainSimulation, QLearningBacteriaTestSimulation
    from adjsim import decision
    from matplotlib import pyplot

    sim = QLearningBacteriaTrainSimulation()
    sim.simulate(10)

    decision.QLearningDecision.print_debug = True
    decision.QLearningDecision.plot_loss_history = True

    sim = QLearningBacteriaTestSimulation()
    sim.simulate(10)

    pyplot.close()