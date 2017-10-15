"""Conway's Game of Life Simulation.

Implementation of Conway's Game of Life (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
"""

from simulation import GosperGliderGun

if __name__ == "__main__":
    sim = GosperGliderGun()
    sim.simulate(100)
