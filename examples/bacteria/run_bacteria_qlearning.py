"""Bacteria Simulation.

Implementation of interaction between bacteria which exhibit agency, and static food.
Bacteria simply must move towards the food and consume it. Bacteria will starve if they run out of 
calories, and they have the ability to divide.
"""

from simulation import QLearningBacteriaTestSimulation

if __name__ == "__main__":    
    sim = QLearningBacteriaTestSimulation()
    sim.simulate(100)
    sim.trackers["agent_count"].plot()