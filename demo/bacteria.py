"""Bacteria Simulation.

Implementation of interaction between bacteria which exhibit agency, and static food.
Bacteria simply must move towards the food and consume it. Bacteria will starve if they run out of 
calories, and they have the ability to divide.
"""

# Standard.
import random, math, sys, os

# Third party.
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from adjsim import core, utility, decision, analysis, color


# Constants.
MOVEMENT_COST = 5
MOVEMENT_BOUND = 70000
CALORIE_UPPER_BOUND_PREDATOR = 200
EAT_DIST_SQUARE = 150
MOVE_DIST = 20


class Bacteria(core.VisualAgent):
    def __init__(self, pos):
        super().__init__()

        self.pos = pos
        self.calories = random.randint(50, 75)
        self.divide_threshold = 75
        self.color = color.GREEN
        self.size = 10

        self.decision = decision.RandomRepeatedCastDecision()

        self.actions["move"] = move
        self.actions["starve"] = starve
        self.actions["eat"] = eat
        self.actions["divide"] = divide
        self.actions["wait"] = wait
        

class Yogurt(core.VisualAgent):
    def __init__(self, pos):
        super().__init__()

        self.pos = pos
        self.calories = random.randint(5, 35)
        self.color = color.PINK
        self.size = 5
        
        self.decision = decision.RandomSingleCastDecision()

        self.actions["wait"] = wait


def eat(simulation, source):
    closest_distance = sys.float_info.max
    nearest_neighbour = None
    for agent in simulation.agents:
        if agent.id == source.id or type(agent) == Bacteria:
            continue

        distance = utility.distance_square(agent, source)
        if distance < closest_distance:
            nearest_neighbour = agent
            closest_distance = distance

    if closest_distance > EAT_DIST_SQUARE:
        return

    source.calories = np.clip(source.calories + nearest_neighbour.calories, 0, CALORIE_UPPER_BOUND_PREDATOR)
    simulation.agents.remove(nearest_neighbour)
    
    source.step_complete = True

def move(simulation, source):
    movement = (np.random.rand(2) - 0.5) * MOVE_DIST
    if np.sum((source.pos + movement)**2) < MOVEMENT_BOUND and source.calories > MOVEMENT_COST:
        source.pos = source.pos + movement
        source.calories -= MOVEMENT_COST
        source.step_complete = True

def starve(simulation, source):
    if source.calories <= MOVEMENT_COST:
        simulation.agents.remove(source)
        source.step_complete = True

def divide(simulation, source):
    if source.calories > source.divide_threshold:
        simulation.agents.add(Bacteria(np.array(source.pos)))

        source.calories -= source.divide_threshold
        source.step_complete = True

def wait(simulation, source):
    source.step_complete = True

def end_condition(simulation):
    num_predators = 0

    for agent in simulation.agents:
        num_predators += 1

    return num_predators == 0


class BacteriaSimulation(core.VisualSimulation):
    def __init__(self):
        super().__init__()

        self.end_condition = end_condition
        self.trackers["agent_count"] = analysis.AgentTypeCountTracker()
        
        # create bacteria agents
        for i in range(5):
            for j in range(5):
                self.agents.add(Bacteria(np.array([10*i, 10*j], dtype=np.float)))

        # create yogurt agents
        for i in range(20):
            for j in range(20):
                self.agents.add(Yogurt(np.array([5*i, 5*j + 50], dtype=np.float)))

    
# AGENT CREATION SCRIPT
if __name__ == "__main__":    
    sim = BacteriaSimulation()
    sim.simulate(100)
    sim.trackers["agent_count"].plot()
