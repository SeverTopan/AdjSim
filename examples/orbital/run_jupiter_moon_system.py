"""Jupiter Moon System Simulation.

Exemplifies implementation of physics into adjsim.
"""

from simulation import JupiterMoonSystemSimulation

if __name__ == "__main__":
    sim = JupiterMoonSystemSimulation()
    sim.simulate(100)
