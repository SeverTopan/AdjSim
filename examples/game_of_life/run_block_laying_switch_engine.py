"""Conway's Game of Life Simulation.

Implementation of Conway's Game of Life (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
"""

from simulation import BlockLayingSwitchEngine

if __name__ == "__main__":
    sim = BlockLayingSwitchEngine()
    sim.simulate(100)
