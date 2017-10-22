"""Bacteria Simulation.

Implementation of interaction between bacteria which exhibit agency, and static food.
Bacteria simply must move towards the food and consume it. Bacteria will starve if they run out of 
calories, and they have the ability to divide.
"""

# Standard.
import random, math, sys, os

# Third party.
import numpy as np
from adjsim import core, utility, decision, analysis, color


# Constants.
MOVEMENT_COST = 5
MOVEMENT_BOUND = 70000
CALORIE_UPPER_BOUND_PREDATOR = 200
EAT_DIST_SQUARE = 150
MOVE_DIST = 20


class Bacteria(core.VisualAgent):
    def __init__(self, pos, decision_):
        super().__init__()

        self.pos = pos
        self.calories = random.randint(50, 75)
        self.divide_threshold = 75
        self.color = color.GREEN
        self.size = 10

        self.move_rho = decision.DecisionMutableFloat(0, MOVE_DIST)
        self.move_theta = decision.DecisionMutableFloat(0, 360)

        self.decision = decision_

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


def find_closest_food(simulation, source):
    closest_distance = sys.float_info.max
    nearest_neighbour = None
    for agent in simulation.agents:
        if agent.id == source.id or type(agent) == Bacteria:
            continue

        distance = utility.distance_square(agent, source)
        if distance < closest_distance:
            nearest_neighbour = agent
            closest_distance = distance

    return (nearest_neighbour, closest_distance)


def bacteria_loss(simulation, source):
    return -source.calories


def bacteria_perception(simulation, source):
    # Find closest food article.
    nearest_food, distance = find_closest_food(simulation, source)

    # Round calories.
    rounded_calories = round(source.calories/10)*10

    # Condition where no food is found.
    # The 4th tuple element puts us in an entirely new state.
    if nearest_food is None:
        return (0, 0, rounded_calories, 0)

    # Obtain theta value.
    delta = nearest_food.pos - source.pos
    theta = math.atan(delta[1]/delta[0]) if delta[0] != 0 else np.sign(delta[1])*math.pi/2

    # Round observation to reduce number of possible states.
    rounded_distance = round(distance/20)*20
    rounded_theta = round(theta/10)*10

    return (rounded_distance, rounded_theta, rounded_calories, 1)
        

def eat(simulation, source):
    nearest_food, distance = find_closest_food(simulation, source)

    if distance > EAT_DIST_SQUARE:
        return

    source.calories = np.clip(source.calories + nearest_food.calories, 0, CALORIE_UPPER_BOUND_PREDATOR)
    simulation.agents.remove(nearest_food)
    
    source.step_complete = True


def move(simulation, source):
    move_rho = source.move_rho.value
    move_theta = source.move_theta.value

    dx = math.cos(move_theta) * move_rho
    dy = math.sin(move_theta) * move_rho

    movement = np.array([dx, dy])

    if source.calories > MOVEMENT_COST:
        source.pos = source.pos + movement
        source.calories -= MOVEMENT_COST
        source.step_complete = True


def starve(simulation, source):
    if source.calories <= MOVEMENT_COST:
        simulation.agents.remove(source)
        source.step_complete = True


def divide(simulation, source):
    if source.calories > source.divide_threshold:
        simulation.agents.add(Bacteria(np.array(source.pos), simulation.bacteria_decision))

        source.calories -= source.divide_threshold
        source.step_complete = True


def wait(simulation, source):
    source.step_complete = True


def end_condition(simulation):
    num_predators = 0

    for agent in simulation.agents:
        num_predators += 1

    return num_predators == 0


class BasicBacteriaSimulation(core.VisualSimulation):
    def __init__(self):
        super().__init__()

        self.end_condition = end_condition
        self.trackers["agent_count"] = analysis.AgentTypeCountTracker()

        self.bacteria_decision = decision.RandomRepeatedCastDecision()
        
        # create bacteria agents
        for i in range(5):
            for j in range(5):
                self.agents.add(Bacteria(np.array([10*i, 10*j], dtype=np.float), self.bacteria_decision))

        # create yogurt agents
        for i in range(20):
            for j in range(20):
                self.agents.add(Yogurt(np.array([5*i, 5*j + 50], dtype=np.float)))

    
class QLearningBacteriaTrainSimulation(core.Simulation):
    def __init__(self):
        super().__init__()

        self.end_condition = end_condition
        self.trackers["agent_count"] = analysis.AgentTypeCountTracker()

        io_file_name = "bacteria_intelligent.qlearning.pkl"
        self.bacteria_decision = decision.QLearningDecision(perception=bacteria_perception, loss=bacteria_loss, 
            callbacks=self.callbacks, input_file_name=io_file_name, output_file_name=io_file_name)
        
        # create bacteria agents
        for i in range(5):
            for j in range(5):
                self.agents.add(Bacteria(np.array([10*i, 10*j], dtype=np.float), self.bacteria_decision))

        # create yogurt agents
        for i in range(20):
            for j in range(20):
                self.agents.add(Yogurt(np.array([5*i, 5*j + 50], dtype=np.float)))


class QLearningBacteriaTestSimulation(core.VisualSimulation):
    def __init__(self):
        super().__init__()

        self.end_condition = end_condition
        self.trackers["agent_count"] = analysis.AgentTypeCountTracker()

        io_file_name = "bacteria_intelligent.qlearning.pkl"
        self.bacteria_decision = decision.QLearningDecision(perception=bacteria_perception, loss=bacteria_loss, 
            callbacks=self.callbacks, input_file_name=io_file_name, output_file_name=io_file_name, nonconformity_probability=0)
        
        # create bacteria agents
        for i in range(5):
            for j in range(5):
                self.agents.add(Bacteria(np.array([10*i, 10*j], dtype=np.float), self.bacteria_decision))

        # create yogurt agents
        for i in range(20):
            for j in range(20):
                self.agents.add(Yogurt(np.array([5*i, 5*j + 50], dtype=np.float)))
