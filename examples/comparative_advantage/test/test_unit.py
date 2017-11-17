import pytest
import math

def test_transaction_equal():
    from examples.comparative_advantage.simulation import TraderSimulation, MediationLogEntry
    import adjsim
    import numpy as np

    traders = [
            ("England", np.array([1/10, 1/12])),
            ("Portugal", np.array([1/9, 1/8]))
        ]

    sim = TraderSimulation(traders)
    sim.trackers["transaction"].data.append([]) # Housekeeping, this will throw later if not here.
    england = sim.trader_index[0]
    portugal = sim.trader_index[1]

    england.commodities = np.array([1., 1.])
    england.trade_amount._set_value(1)
    england.trade_buy_commodity._set_value(0)
    england.trade_sell_commodity._set_value(1)
    england.trade_target_index._set_value(1)
    england.actions["trade_commodity"](sim, england)

    mediation_log_entry = MediationLogEntry.from_agent(england)

    assert sim.transaction_mediation_log.get(mediation_log_entry) == 1
    assert (england.commodities == np.array([1, 0])).all()

    portugal.commodities = np.array([1., 1.])
    portugal.trade_amount._set_value(1)
    portugal.trade_buy_commodity._set_value(1)
    portugal.trade_sell_commodity._set_value(0)
    portugal.trade_target_index._set_value(0)
    portugal.actions["trade_commodity"](sim, portugal)

    assert not sim.transaction_mediation_log
    assert (england.commodities == np.array([2, 0])).all()
    assert (portugal.commodities == np.array([0, 2])).all()


def test_transaction_sell_less():
    from examples.comparative_advantage.simulation import TraderSimulation, MediationLogEntry, Meta
    import adjsim
    import numpy as np

    traders = [
            ("England", np.array([1/10, 1/12])),
            ("Portugal", np.array([1/9, 1/8]))
        ]

    sim = TraderSimulation(traders)
    sim.trackers["transaction"].data.append([]) # Housekeeping, this will throw later if not here.
    england = sim.trader_index[0]
    portugal = sim.trader_index[1]

    england.commodities = np.array([1., 1.])
    england.trade_amount._set_value(1)
    england.trade_buy_commodity._set_value(0)
    england.trade_sell_commodity._set_value(1)
    england.trade_target_index._set_value(1)
    england.actions["trade_commodity"](sim, england)

    mediation_log_entry = MediationLogEntry.from_agent(england)

    assert sim.transaction_mediation_log.get(mediation_log_entry) == 1
    assert (england.commodities == np.array([1, 0])).all()

    portugal.commodities = np.array([1., 1.])
    portugal.trade_amount._set_value(0.5)
    portugal.trade_buy_commodity._set_value(1)
    portugal.trade_sell_commodity._set_value(0)
    portugal.trade_target_index._set_value(0)
    portugal.actions["trade_commodity"](sim, portugal)

    assert sim.transaction_mediation_log.get(mediation_log_entry) == 0.5
    assert (england.commodities == np.array([1.5, 0])).all()
    assert (portugal.commodities == np.array([0.5, 1.5])).all()

    meta = None
    for agent in sim.agents:
        if isinstance(agent, Meta):
            meta = agent
            break
    
    meta.actions["pre_step"](sim, meta)

    assert not sim.transaction_mediation_log
    assert (england.commodities == np.array([1.5, 0.5])).all()
    assert (portugal.commodities == np.array([0.5, 1.5])).all()

def test_transaction_sell_more():
    from examples.comparative_advantage.simulation import TraderSimulation, MediationLogEntry, Meta
    import adjsim
    import numpy as np

    traders = [
            ("England", np.array([1/10, 1/12])),
            ("Portugal", np.array([1/9, 1/8]))
        ]

    sim = TraderSimulation(traders)
    sim.trackers["transaction"].data.append([]) # Housekeeping, this will throw later if not here.
    england = sim.trader_index[0]
    portugal = sim.trader_index[1]

    england.commodities = np.array([1., 1.])
    england.trade_amount._set_value(0.5)
    england.trade_buy_commodity._set_value(0)
    england.trade_sell_commodity._set_value(1)
    england.trade_target_index._set_value(1)
    england.actions["trade_commodity"](sim, england)

    mediation_log_entry = MediationLogEntry.from_agent(england)

    assert sim.transaction_mediation_log.get(mediation_log_entry) == 0.5
    assert (england.commodities == np.array([1, 0.5])).all()

    portugal.commodities = np.array([1., 1.])
    portugal.trade_amount._set_value(1)
    portugal.trade_buy_commodity._set_value(1)
    portugal.trade_sell_commodity._set_value(0)
    portugal.trade_target_index._set_value(0)
    portugal.actions["trade_commodity"](sim, portugal)

    inverse_mediation_log_entry = MediationLogEntry.from_agent(portugal)

    assert sim.transaction_mediation_log.get(mediation_log_entry) is None
    assert sim.transaction_mediation_log.get(inverse_mediation_log_entry) == 0.5
    assert (england.commodities == np.array([1.5, 0.5])).all()
    assert (portugal.commodities == np.array([0, 1.5])).all()

    meta = None
    for agent in sim.agents:
        if isinstance(agent, Meta):
            meta = agent
            break
    
    meta.actions["pre_step"](sim, meta)

    assert not sim.transaction_mediation_log
    assert (england.commodities == np.array([1.5, 0.5])).all()
    assert (portugal.commodities == np.array([0.5, 1.5])).all()

def test_production():
    from examples.comparative_advantage.simulation import TraderSimulation, MediationLogEntry, Meta
    import adjsim
    import numpy as np

    traders = [
            ("England", np.array([1/10, 1/12])),
            ("Portugal", np.array([1/9, 1/8]))
        ]

    sim = TraderSimulation(traders)
    sim.trackers["transaction"].data.append([]) # Housekeeping, this will throw later if not here.
    england = sim.trader_index[0]
    portugal = sim.trader_index[1]

    meta = None
    for agent in sim.agents:
        if isinstance(agent, Meta):
            meta = agent
            break
    
    for i in range(10):
        meta.actions["pre_step"](sim, meta)

        assert (england.commodities == np.zeros(2)).all()
        assert (portugal.commodities == np.zeros(2)).all()

    portugal.production_allocation_assignation._set_value(np.array([1., 1.]))
    portugal.actions["allocate_production"](sim, portugal)
    england.production_allocation_assignation._set_value(np.array([1., 1.]))
    england.actions["allocate_production"](sim, england)

    for i in range(10):
        meta.actions["pre_step"](sim, meta)

    assert (england.commodities == np.array([[1/10, 1/12]])).all()
    assert (portugal.commodities == np.array([1/9, 1/8])).all()


    portugal.production_allocation_assignation._set_value(np.array([1., 1.]))
    portugal.actions["done"](sim, portugal)
    england.production_allocation_assignation._set_value(np.array([1., 1.]))
    england.actions["done"](sim, england)

    for i in range(10):
        meta.actions["pre_step"](sim, meta)

    assert (england.commodities == np.array([[1/10, 1/12]])).all()
    assert (portugal.commodities == np.array([1/9, 1/8])).all()

def test_loss():
    from examples.comparative_advantage.simulation import TraderSimulation, MediationLogEntry, Meta, loss
    import adjsim
    import numpy as np

    traders = [
            ("England", np.array([1/10, 1/12])),
            ("Portugal", np.array([1/9, 1/8]))
        ]

    sim = TraderSimulation(traders)
    sim.trackers["transaction"].data.append([]) # Housekeeping, this will throw later if not here.
    england = sim.trader_index[0]
    portugal = sim.trader_index[1]

    meta = None
    for agent in sim.agents:
        if isinstance(agent, Meta):
            meta = agent
            break
    
    for i in range(10):
        meta.actions["pre_step"](sim, meta)

        assert loss(sim, england) == 0
        assert loss(sim, portugal) == 0

        assert (england.previous_commodities == np.zeros(2)).all()
        assert (portugal.previous_commodities == np.zeros(2)).all()

    portugal.production_allocation_assignation._set_value(np.array([1., 1.]))
    portugal.actions["allocate_production"](sim, portugal)
    england.production_allocation_assignation._set_value(np.array([1., 1.]))
    england.actions["allocate_production"](sim, england)

    # Change sim time so that loss isnt short circuited.
    sim.time = 2

    meta.actions["pre_step"](sim, meta)

    assert (england.commodities == np.array([1/10, 1/12])).all()
    assert (portugal.commodities == np.array([1/9, 1/8])).all()

    assert (england.previous_commodities == np.zeros(2)).all()
    assert (portugal.previous_commodities == np.zeros(2)).all()

    assert math.isclose(loss(sim, england), -(1/10 + 1/12) / 2)
    assert math.isclose(loss(sim, portugal), -(1/9 + 1/8) / 2)

    assert (england.previous_commodities == np.array([1/10, 1/12])).all()
    assert (portugal.previous_commodities == np.array([1/9, 1/8])).all()

    portugal.production_allocation_assignation._set_value(np.array([1., 1.]))
    portugal.actions["done"](sim, portugal)
    england.production_allocation_assignation._set_value(np.array([1., 1.]))
    england.actions["done"](sim, england)

    for i in range(10):
        meta.actions["pre_step"](sim, meta)

    assert loss(sim, england) == 0
    assert loss(sim, portugal) == 0