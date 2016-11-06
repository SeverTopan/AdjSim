AdjSim Simulation Framework
===========================

A simple simulation framework. Intended for simulation of ecosystems.

---

Current Development State
-------------------------

AdjSim is currently in its early stages of development. There are four core elements of the simulation framework that are envisioned.

 1. The first is the computation involved in agent interaction through ability casting and timestep iteration.
 2. The second is a translation module. The aim is to be able to write simulation scripts in a simple language (see sampleScript for a rough example) and have AdjSim translate it into the class structures it needs internally.
 3. The third core element is a simple graphical representation of the simulation script.
 4. The final core functionality is the decision making module for simulation agents. Agents will be able to choose which abilities to cast when. I am currently considering doing this with a genetic algorithm, testing possible ability combinations at each timestep and performing the one that maximizes the desires of each agent.

Currently Implemented Features:
 - Core functionality - agent interaction through ability casting, timestep iterations
 - Core functionality - Graphical representation using PyQt4

Planned Features:
 - Improvement of agent interaction to reflect the framework structure listed below better.
 - More test cases!
 - Core functionality - translation module
 - Core functionality - decision module

---

Running AdjSim
--------------

Clone the repository and run python 3 on the AdjSim folder:

     git clone https://github.com/SeverTopan/AdjSim.github
     cd AdjSim
     python3 AdjSim/

Currently the main execution script calls the bacteria/yogurt test case. It simulates the behavior of a set of bacteria exposed to a parcel of food (in this case yogurt).

AdjSim also uses pyqt4 for its graphical simulation space representation. Obtain Using:

     sudo apt-get install python3-pyqt4

---

Framework Structure
-------------------

The goal of this structure is to keep the fundamentals of a simulation in a simple, organized structure that can be used to simulate many different situations. It is essentially up to the writer of the simulation script. I aim to post more test cases to exemplify the versatility of the structure.

**Agents**: The AdjSim environment can be thought of as a file system. The folders in this file system are agents. They are meant to represent a simulation entity, such as an electron, or a bacterium.

**Traits**: AdjSim agents, like folders, contain data via 'traits', which are name - value pairs. Trait values can take on any type, including other agents! The same way a folder can contain another folder, an agent representing a dog can contain separate agents for its legs, body, head and tail.

**Abilities**: Agents interact with each other using abilities. Abilities perform a set of effects when a condition is fulfilled. In the simplest test case provided, a 'dog' agent performs an 'eat' ability on an 'apple' agent if it is within range. The effects of the ability involve removing the apple, and having the dog consume the calories contained within the apple. Abilities are also traits, and can be added, removed, or modified.

A more detailed description of the Framework structure will be posted once the translation module is implemented.

---

> Designed and developed by Sever Topan
