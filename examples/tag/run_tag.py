"""Tag Game Simulation.

One of the most simple simulations. One Agent is "it" and can transfer the state of being "it" to 
other agents by taggeing them. Agent count remains constant.
"""

from simulation import TaggerSimulation

if __name__ == "__main__":
    sim = TaggerSimulation()
    sim.simulate(100)
