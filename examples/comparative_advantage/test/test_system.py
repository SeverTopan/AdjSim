import pytest

def test_comparative_advantage():
    from examples.comparative_advantage.simulation import TraderSimulation
    import numpy as np

    traders = [
            ("England", np.array([1/10, 1/12])),
            ("Portugal", np.array([1/9, 1/8]))
        ]

    sim = TraderSimulation(traders)
    sim.simulate(10)

