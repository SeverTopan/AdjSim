from adjsim import decision
from simulation import TraderSimulation
import numpy as np

def run(length):
    traders = [
            ("England", np.array([1/10, 1/12])),
            ("Portugal", np.array([1/9, 1/8]))
        ]

    sim = TraderSimulation(traders)
    sim.simulate(length)
    return sim

if __name__ == "__main__":

    for _ in range(10):
        run(1000)
    
    decision.QLearningDecision.print_debug = True
    decision.QLearningDecision.plot_loss_history = True
    sim = run(1000)
    sim.trackers["transaction"].plot()