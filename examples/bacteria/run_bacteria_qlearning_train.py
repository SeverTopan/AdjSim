"""Bacteria Simulation.

Implementation of interaction between bacteria which exhibit agency, and static food.
Bacteria simply must move towards the food and consume it. Bacteria will starve if they run out of 
calories, and they have the ability to divide.
"""

from simulation import QLearningBacteriaTrainSimulation, QLearningBacteriaTestSimulation

if __name__ == "__main__":    
    # Initial test.
    sim = QLearningBacteriaTestSimulation()
    sim.simulate(50)
    sim.trackers["agent_count"].plot()

    # Train.
    epochs = 100
    for _ in range(epochs):
        sim = QLearningBacteriaTrainSimulation()
        sim.simulate(350)