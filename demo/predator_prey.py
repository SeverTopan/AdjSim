
# standard
import random, math, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# third party
import numpy as np
from adjsim import simulation, utility, decision, color


# CONSTANTS
MOVEMENT_COST = 8
PHOTOSYNTHESIS_AMOUNT = 15
PHOTOSYNTHESIS_BLOCK_RANGE = 5
MOVEMENT_BOUND = 70000
CALORIE_UPPER_BOUND_PREDATOR = 400
CALORIE_UPPER_BOUND_PREY = 100
EAT_DIST_SQUARE = 150
MOVE_DIST = 20


class Predator(simulation.VisualAgent):
    def __init__(self, pos):
        super().__init__()

        self.pos = pos
        self.calories = random.randint(50, 75)
        self.divide_threshold = 125
        self.color = color.RED_DARK
        self.size = 10

        self.decision = decision.RandomRepeatedCastDecision()

        self.actions["move"] = move
        self.actions["starve"] = starve
        self.actions["eat"] = eat
        self.actions["divide"] = divide
        self.actions["wait"] = wait


class Prey(simulation.VisualAgent):
    def __init__(self, pos):
        super().__init__()

        self.pos = pos
        self.calories = random.randint(5, 35)
        self.divide_threshold = 40
        self.size = 5
        
        self.decision = decision.RandomRepeatedCastDecision()

        self.actions["move"] = move
        self.actions["photosynthesize"] = photosynthesize
        self.actions["divide"] = divide
        self.actions["wait"] = wait


def eat(simulation, source):
    closest_distance = sys.float_info.max
    nearest_neighbour = None
    for agent in simulation.agents:
        if agent.id == source.id or type(agent) == Predator:
            continue

        distance = utility.distance_square(agent, source)
        if distance < closest_distance:
            nearest_neighbour = agent
            closest_distance = distance

    if closest_distance > EAT_DIST_SQUARE:
        return

    print(nearest_neighbour in simulation.agents)

    source.calories = np.clip(source.calories + nearest_neighbour.calories, 0, CALORIE_UPPER_BOUND_PREDATOR)
    simulation.agents.remove(nearest_neighbour)
    print(nearest_neighbour in simulation.agents)
    
    source.step_complete = True

def move(simulation, source):
    movement = (np.random.rand(2) - 0.5) * MOVE_DIST
    if np.sum((source.pos + movement)**2) < MOVEMENT_BOUND and source.calories > MOVEMENT_COST:
        source.pos += movement
        source.calories -= MOVEMENT_COST
        source.step_complete = True 

def starve(simulation, source):
    if source.calories <= MOVEMENT_COST:
        simulation.agents.remove(source)
        source.step_complete = True

def divide(simulation, source):
    if source.calories > source.divide_threshold:
        if type(source) == Predator:
            simulation.agents.add(Predator(source.pos))
        else:
            simulation.agents.add(Prey(source.pos))

        source.calories -= source.divide_threshold
        source.step_complete = True

def photosynthesize(simulation, source):
    source.calories = np.clip(source.calories + PHOTOSYNTHESIS_AMOUNT, 0, CALORIE_UPPER_BOUND_PREY)
    source.step_complete = True

def wait(simulation, source):
    source.step_complete = True


class PredatorPreySimulation(simulation.VisualSimulation):
    def __init__(self):
        super().__init__()
        thetaValues = [x*0.2 for x in range(1, 32)]

        # create predator agents
        SPACING = 75
        for theta in thetaValues:
            for d in range(1,3):
                new_agent = Predator(np.array([d*SPACING*math.cos(theta), d*SPACING*math.sin(theta)]))
                self.agents.add(new_agent)


        # create prey agents
        SPACING = 25
        for theta in thetaValues:
            for d in range(1,10):
                new_agent = Prey(np.array([d*SPACING*math.cos(theta), d*SPACING*math.sin(theta)]))
                self.agents.add(new_agent)

    
# AGENT CREATION SCRIPT
if __name__ == "__main__":    
    sim = PredatorPreySimulation()
    sim.simulate(100)
