# AdjSim Simulation Framework
[![Build Status](https://travis-ci.org/SeverTopan/AdjSim.svg?branch=master)](https://travis-ci.org/SeverTopan/AdjSim) [![Coverage Status](https://coveralls.io/repos/github/SeverTopan/AdjSim/badge.svg?branch=master)](https://coveralls.io/github/SeverTopan/AdjSim?branch=master) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A simulation framework. Intended for simulation of ecosystems.


> Designed and developed by Sever Topan

## Features

### Engine

At its core, AdjSim is an agent-based modelling engine. It allows users to define simulation environments through which agents interact through ability casting and timestep iteration. The framework is targeted towards agents that behave intelligently, for example a bacterium chasing down food. However, the framework is extremely flexible - from enabling physics simulation to defining an environment in which [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) plays out!

### Graphical Simulation Representation

The simulation can be viewed in real time as it unfolds, with graphics are rendered and animated using PyQt5. Below are  four of the distinct demos packadged with AdjSim, ranging from bacteria to moon system simulation.

 | ![Bacteria Demo](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/demo/images/readme_bacteria.png)| ![Predator Prey Demo](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/demo/images/readme_predator_prey.png) |
|:-------------:|:-------------:|
| ![GOL Demo](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/demo/images/readme_game_of_life.png) | ![Jupiter Demo](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/demo/images/readme_jupiter_moon_system.png) |

### Post Simulation Analysis Tools

Agent properties can be marked for tracking during simulation, allowing for viewing the results of these values once the simulation completes. For example, we can track the population of each different type of agent, or the efficacy of the agent's ability to meet its intelligence module-defined goals.

| ![QLearning Graph](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/demo/images/readme_individual_learning.png)| ![Predator Prey Graph](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/demo/images/readme_predator_prey_population.png) |
|:-------------:|:-------------:|

### Intelligence Module

Perhaps the most computationally interesting aspect of AdjSim lies in its intelligence module. It allows agents to set goals (for example, the goal of a bacterium may be to maximize its calories), and assess its actions in terms of its ability to meet its goals. This allows the agents to learn which actions are best used in a given situation. Currently the intelligence module implements [Q-Learning](https://en.wikipedia.org/wiki/Q-learning), but more advanced reinforcement learning techniques are coming soon!

## Current Development State

Currently Implemented Features:
 - Core functionality - agent interaction through ability casting, timestep iterations
 - Core functionality - graphical representation using PyQt5
 - Core functionality - AdjSim Framework interface

Partially Implemented Features:
 - Core functionality - post-simulation analysis tools
 - Core functionality - intelligence module

Planned Features:
 - More test cases!
 - More refined API interface, possibly based on Class overloading


## Installing and Running AdjSim

It is reccommended to run AdjSim using virtual python environments provided by Anaconda or Pip. The following describes the installation procedure for each of these.

Clone the GitHub repository.

     git clone https://github.com/SeverTopan/AdjSim

Make sure Python 3.5 or greater are installed, then create a new environment with it.

    # If using Virtualenv
    virtualenv --python=/usr/bin/python3.6 venv
    source venv/bin/activate

    # If using Anaconda
    conda create --name adjsim python=3.6
    activate adjsim

Install Dependencies.

     python setup.py install

Note: If you run into trouble importing PyQt5 when installing using the setup.py file, try using

    pip install -e .

## Framework Structure

The goal of this structure is to keep the fundamentals of a simulation in a simple, organized structure that can be used to simulate many different situations. It is essentially up to the writer of the simulation script. I aim to post more test cases to exemplify the versatility of the structure.

**Agents:** The AdjSim environment can be thought of as a file system. The folders in this file system are agents. They are meant to represent a simulation entity, such as an electron, or a bacterium.

**Traits:** AdjSim agents, like folders, contain data via 'traits', which are name - value pairs. Trait values can take on any type, including other agents! The same way a folder can contain another folder, an agent representing a dog can contain separate agents for its legs, body, head and tail.

**Abilities:** Agents interact with each other using abilities. Abilities perform a set of effects when a condition is fulfilled. In the simplest test case provided, a 'bacterium' agent performs an 'eat' ability on a 'yogurt' agent if it is within range. The effects of the ability involve removing the yogurt, and having the bacterium consume the calories contained within the yogurt parcel. Abilities are also traits, and can be added, removed, or modified.

A more detailed description of the Framework structure will be posted soon.


