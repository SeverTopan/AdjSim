# AdjSim Simulation Framework

A simple simulation framework. Intended for simulation of ecosystems.

## Current Development State

AdjSim is currently in its early stages of development. There are five core elements of the simulation framework that are envisioned.

 1. The first is the computation involved in agent interaction through ability casting and timestep iteration.
 2. The second is a refined Framework interface for AdjSim to be used in python scripts.
 3. A simple graphical representation of the simulation as it unfolds.
 4. Tools to analyze the simulation results after completion.
 5. The final core functionality is the decision making module for simulation agents. Agents will be able to choose which abilities to cast when. I am currently considering doing this with a genetic algorithm, testing possible ability combinations at each timestep and performing the one that maximizes the desires of each agent.

Currently Implemented Features:
 - Core functionality - agent interaction through ability casting, timestep iterations
 - Core functionality - graphical representation using PyQt5
 - Core functionality - AdjSim Framework interface

Partially Implemented Features:
 - Core functionality - post-simulation analysis tools
 - Core functionality - decision module

Planned Features:
 - More test cases!
 - More refined API interface, possibly based on Class overloading


## Installing and Running AdjSim

It is reccommended to run AdjSim using virtual python environments provided by Anaconda or Pip. The following describes the installation procedure for each of these.

### Using Pip/Virtualenv

Clone the GitHub repository.

     git clone https://github.com/SeverTopan/AdjSim

Make sure Python 3.5 or greater are installed, then create a new virtualenv with it.

     virtualenv --python=/usr/bin/python3.6 venv
     source venv/bin/activate

Install Dependencies.

     python setup.py install

### Using Anaconda

Clone the GitHub repository.

     git clone https://github.com/SeverTopan/AdjSim

Create a new Anaconda environment with a python of version 3.5 or greater.

     conda create --name adjsim python=3.6
     activate adjsim

Install Dependencies.

     python setup.py install

## Framework Structure

The goal of this structure is to keep the fundamentals of a simulation in a simple, organized structure that can be used to simulate many different situations. It is essentially up to the writer of the simulation script. I aim to post more test cases to exemplify the versatility of the structure.

**Agents:** The AdjSim environment can be thought of as a file system. The folders in this file system are agents. They are meant to represent a simulation entity, such as an electron, or a bacterium.

**Traits:** AdjSim agents, like folders, contain data via 'traits', which are name - value pairs. Trait values can take on any type, including other agents! The same way a folder can contain another folder, an agent representing a dog can contain separate agents for its legs, body, head and tail.

**Abilities:** Agents interact with each other using abilities. Abilities perform a set of effects when a condition is fulfilled. In the simplest test case provided, a 'bacterium' agent performs an 'eat' ability on a 'yogurt' agent if it is within range. The effects of the ability involve removing the yogurt, and having the bacterium consume the calories contained within the yogurt parcel. Abilities are also traits, and can be added, removed, or modified.

A more detailed description of the Framework structure will be posted soon.


> Designed and developed by Sever Topan
