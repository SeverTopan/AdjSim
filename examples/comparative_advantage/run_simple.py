from adjsim import decision
from simulation import TraderSimulation
import numpy as np

def run(length):
    traders = [
            ("England", np.array([1/10, 1/12])),
            ("Portugal", np.array([1/9, 1/8]))
        ]

    sim = TraderSimulation(traders, is_training=False)
    sim.simulate(length)
    return sim

if __name__ == "__main__":

    decision.QLearningDecision.print_debug = True
    sim = run(1000)
    sim.trackers["transaction"].plot()
    sim.trackers["allocation"].plot()
    sim.trackers["qlearning_England"].plot()
    sim.trackers["qlearning_Portugal"].plot()