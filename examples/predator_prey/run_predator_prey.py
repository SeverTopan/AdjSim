"""Predator-Prey Simulation.

This simulation exemplifies predator-prey relationships
(https://globalchange.umich.edu/globalchange1/current/lectures/predation/predation.html).
The Prey photosynthesizes its calories while predators must approach prey and consume them.
"""

from simulation import PredatorPreySimulation

if __name__ == "__main__":    
    sim = PredatorPreySimulation()
    sim.simulate(100)
