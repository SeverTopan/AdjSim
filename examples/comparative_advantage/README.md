# Comparative Advantage Simulation

This simulation illustrates the phenomenon of [Ricardian Comparative Advantage](https://en.wikipedia.org/wiki/Comparative_advantage) in a free market trading environment. The `run_*` files will trigger the classic trade model between England and Portugal. We can see that though Portugal can produce more of each commodity faster than England, the trading agents mutually benefit from trade rather than production in autarky. Each agent specializes in the production that it happens to be the best at, and global commodity production is increased.

The agents are given a loss function coinciding with the average of their commodities, and they learn the optimal behaviour via [Perturbative Q-Learning](https://severtopan.github.io/AdjSim/adjsim.html?highlight=perturbative#adjsim.decision.PerturbativeQLearningDecision).

 ![comparative_advantage_trade_log](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/gallery/images/comparative_advantage_trade_log.png)

 | ![comparative_advantage_england_production_allocation_average](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/gallery/images/comparative_advantage_england_production_allocation_average.png)| ![comparative_advantage_england_production_allocation_raw](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/gallery/images/comparative_advantage_england_production_allocation_raw.png) |
|:-------------:|:-------------:|
| ![comparative_advantage_england_production_allocation_average](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/gallery/images/comparative_advantage_england_production_allocation_average.png) | ![comparative_advantage_england_production_allocation_raw](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/gallery/images/comparative_advantage_england_production_allocation_raw.png) |