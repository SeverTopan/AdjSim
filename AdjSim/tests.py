#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import random
from environment import *
from constants import *
from PyQt4 import QtGui, QtCore

# FUNCTION GENERATE TEST CLASSES - GAME OF LIFE
#-------------------------------------------------------------------------------
def generateTestClasses_gameOfLife(environment, identifier):

    CELL_SIZE = 5

    # function calculateNeighbours
    # !!! predicates will be grouped together for ease of writing
    # !!! always sort predicate list before insertion into class
    def calculateNeighbours_predicate_self(target):
        return target.abilities['calculateNeighbours'].blockedDuration is 0

    def calculateNeighbours_predicate_env(target):
        return True

    calculateNeighbours_predicateList = [(0, calculateNeighbours_predicate_env), \
        (1, calculateNeighbours_predicate_self)]

    calculateNeighbours_condition = lambda targets: True

    def calculateNeighbours_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        x = targets[1].xCoord
        y = targets[1].yCoord

        neighbourSet = set()
        possibleNeighbourSet = {(x, y + CELL_SIZE),
                        (x, y - CELL_SIZE),
                        (x + CELL_SIZE, y),
                        (x - CELL_SIZE, y),
                        (x + CELL_SIZE, y + CELL_SIZE),
                        (x - CELL_SIZE, y + CELL_SIZE),
                        (x + CELL_SIZE, y - CELL_SIZE),
                        (x - CELL_SIZE, y - CELL_SIZE)}


        # scan for adjacent agents and store into neighbourSet set
        for agent in targets[0].agentSet:
            # ignore environment and self
            if agent is targets[0] or agent is targets[1]:
                continue

            # check bounding boxes
            if agent.xCoord > x + CELL_SIZE or agent.xCoord < x - CELL_SIZE \
                or agent.yCoord > y + CELL_SIZE or agent.yCoord < y - CELL_SIZE:
                continue

            for targetX, targetY in possibleNeighbourSet:
                if agent.xCoord == targetX and agent.yCoord == targetY:
                    neighbourSet.add((agent.xCoord, agent.yCoord));

        # record empty agents within agentSet
        emptyNeighbourSet = possibleNeighbourSet - neighbourSet

        for item in emptyNeighbourSet:
            if targets[0].traits['emptyNeighboursDict'].value.get(item) is None:
                targets[0].traits['emptyNeighboursDict'].value[item] = 1
            else:
                targets[0].traits['emptyNeighboursDict'].value[item] += 1

        # record num neighbours
        targets[1].traits['numNeighbours'].value = len(neighbourSet)

        targets[1].abilities['calculateNeighbours'].blockedDuration = 1


    # ability - environent - add new
    # !!! predicates will be grouped toget\er for ease of writing
    # !!! always sort predicate list before insertion into class
    def addNewAgents_predicate_self(target):
        return target.abilities['addNewAgents'].blockedDuration is 0

    def addNewAgents_predicate_env(target):
        return True

    addNewAgents_predicateList = [(0, addNewAgents_predicate_env), \
        (1, addNewAgents_predicate_self)]

    addNewAgents_condition = lambda targets: True

    def addNewAgents_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        # delete agents
        targets[1].agentSet = {agent for agent in targets[1].agentSet \
            if agent is targets[1] \
            or agent.traits['numNeighbours'].value is 2 \
            or agent.traits['numNeighbours'].value is 3 }

        # add new agents
        emptyNeighboursDict = targets[0].traits['emptyNeighboursDict'].value
        for key, value in emptyNeighboursDict.items():
            if value is 3:
                createCell(targets[1], key[0], key[1])

        emptyNeighboursDict.clear()

        targets[1].abilities['addNewAgents'].blockedDuration = 1

    def createCell(environment, x, y):
        cell = Agent(environment, "cell", x, y)
        cell.addTrait('type', 'live_cell')
        cell.addTrait('numNeighbours', 0)
        cell.size = CELL_SIZE
        cell.color = QtGui.QColor(BLUE_DARK)
        environment.agentSet.add(cell)

        cell.abilities["calculateNeighbours"] = Ability(environment, "calculateNeighbours", cell, \
            calculateNeighbours_predicateList, calculateNeighbours_condition, \
            calculateNeighbours_effect)


    # creation script
    initialCondition_glider = [(0,0),(-1,1),(-1,2),(-2,1),(-2,0)]
    initialCondition_block = [(0,0),(1,0),(0,1),(1,1)]
    initialCondition_blinker = [(0,0),(1,0),(2,0)]
    initialCondition_blockLayingSwitchEngine = [(0,0),                          # 1st column
                                                (2,0),(2,1),                    # 2nd column
                                                (4,2),(4,3),(4,4),              # 3rd column
                                                (6,3),(6,4),(6,5),(7,4)]        # 4th column
    initialCondition_gosperGliderGun = [(0,0),(1,0),(1,1),(0,1),                                            # left-most block
                                        (10,0),(10,1),(10,-1),(11,2),(11,-2),(12,3),(12,-3),(13,3),(13,-3), # curve on left
                                        (14,0),(15,2),(15,-2),(16,1),(16,-1),(16,0),(17,0),                 # 'play button' on left
                                        (20,1),(20,2),(20,3),(21,1),(21,2),(21,3),(22,0),(22,4),            # 2x3 + 2 on right
                                        (24,-1),(24,0),(24,4),(24,5),                                       # trailing 'winglets' on right
                                        (34,2),(34,3),(35,2),(35,3)]                                        # right-most block

    chosenInitialCondition = None
    if identifier == 'gosperGliderGun':
        chosenInitialCondition = initialCondition_gosperGliderGun
    elif identifier == 'blockLayingSwitchEngine':
        chosenInitialCondition = initialCondition_blockLayingSwitchEngine
    else:
        raise Exception('Invalid Identifier')

    for coord in chosenInitialCondition:
        createCell(environment, coord[0] * CELL_SIZE, coord[1] * CELL_SIZE)

    environment.addTrait('emptyNeighboursDict', {})
    environment.abilities['addNewAgents'] = Ability(environment, "addNewAgents", environment, \
        addNewAgents_predicateList, addNewAgents_condition, \
        addNewAgents_effect)



# FUNCTION GENERATE TEST CLASSES - PLANETS
#-------------------------------------------------------------------------------
def generateTestClasses_planets(environment, identifier):

    GRAV_CONSTANT = 6.674e-11
    TIMESTEP_LENGTH = 10000
    DISTANCE_MULTIPLIER = 10000000

    # ability - setup
    # !!! predicates will be grouped toget\er for ease of writing
    # !!! always sort predicate list before insertion into class
    def calculateSetup_predicate_self(target):
        if target.traits.get('type') is not None \
            and target.traits.get('castLog_acc') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['calculateSetup'].blockedDuration is 0:
            return True
        else:
            return False

    def calculateSetup_predicate_env(target):
        return True

    calculateSetup_predicateList = [(0, calculateSetup_predicate_env), \
        (1, calculateSetup_predicate_self)]


    calculateSetup_condition = lambda targets: True

    def calculateSetup_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        targets[1].traits['xAcc'].value = 0;
        targets[1].traits['yAcc'].value = 0;

        targets[1].traits['castLog_acc'].value.clear()

        targets[1].abilities['calculateSetup'].blockedDuration = 1
        targets[1].abilities['calculateAcc'].blockedDuration = 0
        targets[1].abilities['calculateVel'].blockedDuration = 0



    # ability - calculate acceleration
    # !!! predicates will be grouped together for ease of writing
    # !!! always sort predicate list before insertion into class
    def calculateAcc_predicate_target(env, sel, target):
        if target is not env \
            and target is not sel \
            and target.traits.get('type') is not None \
            and target.traits.get('mass') is not None:
            return True
        else:
            return False

    def calculateAcc_predicate_self(target):
        if target.traits.get('type') is not None \
            and target.traits.get('castLog_acc') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['calculateAcc'].blockedDuration is 0:
            return True
        else:
            return False

    def calculateAcc_predicate_env(target):
        return True

    calculateAcc_predicateList = [(0, calculateAcc_predicate_env), \
        (1, calculateAcc_predicate_self), \
        (2, calculateAcc_predicate_target)]


    calculateAcc_condition = lambda targets: targets[2].traits['type'].value is 'planet' \
        and not targets[1].traits['castLog_acc'].value & {targets[2]} \
        and targets[0].traits['numPhysicsDependentAgents'].value > len(targets[1].traits['castLog_acc'].value)

    def calculateAcc_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        xDist = (targets[2].xCoord - targets[1].xCoord) * DISTANCE_MULTIPLIER
        yDist = (targets[2].yCoord - targets[1].yCoord) * DISTANCE_MULTIPLIER
        absDist = (xDist**2 + yDist**2)**0.5
        absAcc = targets[2].traits['mass'].value * GRAV_CONSTANT / (absDist**2)

        targets[1].traits['xAcc'].value += absAcc * (xDist / absDist)
        targets[1].traits['yAcc'].value += absAcc * (yDist / absDist)

        targets[1].traits['castLog_acc'].value.add(targets[2])


    # ability - calculate velocity
    # !!! predicates will be grouped together for ease of writing
    # !!! always sort predicate list before insertion into class
    def calculateVel_predicate_self(target):
        if target.traits.get('type') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['calculateVel'].blockedDuration is 0:
            return True
        else:
            return False

    def calculateVel_predicate_env(target):
        return True

    calculateVel_predicateList = [(0, calculateVel_predicate_env), \
        (1, calculateVel_predicate_self)]

    calculateVel_condition = lambda targets: \
        targets[0].traits['numPhysicsDependentAgents'].value - 1 == len(targets[1].traits['castLog_acc'].value)

    def calculateVel_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        targets[1].traits['xVel'].value += targets[1].traits['xAcc'].value * TIMESTEP_LENGTH
        targets[1].traits['yVel'].value += targets[1].traits['yAcc'].value * TIMESTEP_LENGTH

        targets[1].xCoord += targets[1].traits['xVel'].value * TIMESTEP_LENGTH / DISTANCE_MULTIPLIER
        targets[1].yCoord += targets[1].traits['yVel'].value * TIMESTEP_LENGTH / DISTANCE_MULTIPLIER

        targets[1].abilities['calculateAcc'].blockedDuration = 2
        targets[1].abilities['calculateVel'].blockedDuration = 2

    def createPlanet(name, mass, size, color, xPos, yPos, xVel, yVel, environment, style = QtCore.Qt.SolidPattern):
        planet = Agent(environment, name, xPos, yPos)
        planet.addTrait('type', 'planet')
        planet.addTrait('xVel', xVel)
        planet.addTrait('yVel', yVel)
        planet.addTrait('xAcc', 0.0)
        planet.addTrait('yAcc', 0.0)
        planet.addTrait('mass', mass)
        planet.addTrait('castLog_acc', set())
        planet.size = size
        planet.color = color
        planet.style = style

        planet.abilities["calculateSetup"] = Ability(environment, "calculateSetup", planet, \
            calculateSetup_predicateList, calculateSetup_condition, calculateSetup_effect)
        planet.abilities["calculateAcc"] = Ability(environment, "calculateAcc", planet, \
            calculateAcc_predicateList, calculateAcc_condition, calculateAcc_effect)
        planet.abilities["calculateVel"] = Ability(environment, "calculateVel", planet, \
            calculateVel_predicateList, calculateVel_condition, calculateVel_effect)
        planet.abilities["calculateAcc"].blockedDuration = 2
        planet.abilities["calculateVel"].blockedDuration = 2

        environment.agentSet.add(planet)

    if identifier == 'earth':
        # earth/moon
        createPlanet('earth', 5.972e24, 5, QtGui.QColor(BLUE_DARK), 0, 0, 0.0 , 0, environment)
        createPlanet('moon', 7.3e22, 3, QtGui.QColor(GREY), 38, 0, 0.0, 1.02e3, environment)

        environment.addTrait('numPhysicsDependentAgents', 2)

    elif identifier == 'jupiter':
        # jupiter system
        createPlanet('jupiter', 1.898e27, 10, QtGui.QColor(ORANGE), 0, 0, 0.0 , 0, environment, QtCore.Qt.Dense1Pattern)
        createPlanet('io', 8.9e22, 3, QtGui.QColor(GREY), 42, 0, 0.0, 17.38e3, environment)
        createPlanet('europa', 4.8e22, 3, QtGui.QColor(BLUE_LIGHT), 67, 0, 0.0, 13.7e3, environment)
        createPlanet('ganymede', 1.48e23, 5, QtGui.QColor(RED_DARK), 107, 0, 0.0, 10.88e3, environment)
        createPlanet('callisto', 1.08e23, 4, QtGui.QColor(BROWN_LIGHT), 188, 0, 0.0, 8.21e3, environment)

        environment.addTrait('numPhysicsDependentAgents', 5)

    else:
        raise Exception('Unknown test case identifier')

# FUNCTION GENERATE TEST CLASSES - BACTERIA YOGURT
#-------------------------------------------------------------------------------
def generateTestClasses_bacteriaYogurt(environment):

    MOVEMENT_COST = 5

    # ability eat condition: food.type is 'food'
    #       && ((food.x - self.x)^2 + (food.y - self.y)^2)^0.5 < self.eatRange
    # !!! predicates will be grouped together for ease of writing
    # !!! always sort predicate list before insertion into class
    def eat_predicate_food(env, sel, target):
        if target.traits.get('type') is not None \
            and target.xCoord < sel.xCoord + sel.traits.get('interactRange').value \
            and target.xCoord > sel.xCoord - sel.traits.get('interactRange').value \
            and target.yCoord < sel.yCoord + sel.traits.get('interactRange').value \
            and target.yCoord > sel.yCoord - sel.traits.get('interactRange').value \
            and target.traits.get('calories') is not None:
            return True
        else:
            return False

    def eat_predicate_self(target):
        if target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['eat'].blockedDuration is 0:
            return True
        else:
            return False

    def eat_predicate_env(target):
        return True

    eat_predicateList = [(0, eat_predicate_env), \
        (1, eat_predicate_self), \
        (2, eat_predicate_food)]

    eat_condition = lambda targets: targets[2].traits['type'].value is 'food' \
        and ((targets[2].traits['xCoord'].value - targets[1].traits['xCoord'].value)**2 \
        + (targets[2].traits['yCoord'].value - targets[1].traits['yCoord'].value)**2)**0.5 \
        < targets[1].traits['interactRange'].value

    def eat_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        targets[1].traits['calories'].value += targets[2].traits['calories'].value

        targets[0].agentSet.remove(targets[2])
        targets[1].blockedDuration = 1

    # ability - move
    def move_predicate_self(target):
        if target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['move'].blockedDuration is 0 \
            and target.blockedDuration is 0:
            return True
        else:
            return False
    move_predicateList = [(1, move_predicate_self)]

    move_condition = lambda targets: targets[1].traits['calories'].value > MOVEMENT_COST

    def move_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        targets[1].traits['calories'].value -= MOVEMENT_COST

        randX = random.uniform(-1, 1)
        randY = random.uniform(-1, 1)
        absRand = (randX**2 + randY**2)**0.5
        movementMultiplier = targets[1].traits['interactRange'].value * 2

        dx = (randX / absRand) * movementMultiplier
        dy = (randY / absRand) * movementMultiplier

        targets[1].yCoord += dy
        targets[1].xCoord += dx

        targets[1].abilities['move'].blockedDuration = 1

    # ability - starve
    def starve_predicate_self(target):
        if target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0:
            return True
        else:
            return False
    starve_predicateList = [(1, starve_predicate_self)]

    starve_condition = lambda targets: targets[1].traits['calories'].value <= MOVEMENT_COST

    def starve_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        targets[0].agentSet.remove(targets[1])
        targets[1].blockedDuration = 1

    # ability - divide
    def divide_predicate_self(target):
        if target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['divide'].blockedDuration is 0:
            return True
        else:
            return False

    def divide_predicate_env(target):
        return True

    divide_predicateList = [(0, divide_predicate_env), (1, divide_predicate_self)]

    divide_condition = lambda targets: targets[1].traits['calories'].value > 150

    def divide_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        targets[1].traits['calories'].value -= 75
        targets[1].blockedDuration = 2

        bacterium = Agent(environment, "bacterium_child", targets[1].xCoord + 10, targets[1].yCoord)
        bacterium.addTrait('type', 'bacteria')
        bacterium.addTrait('calories', 75)
        bacterium.addTrait('interactRange', 10)
        bacterium.blockedDuration = 2
        bacterium.size = 10
        bacterium.color = QtGui.QColor(GREEN)
        targets[0].traits['agentSet'].value.add(bacterium)

        bacterium.abilities["divide"] = Ability(environment, "divide", bacterium, \
            divide_predicateList, divide_condition, divide_effect)
        bacterium.abilities["eat"] = Ability(environment, "eat", bacterium, eat_predicateList, \
            eat_condition, eat_effect)
        bacterium.abilities["move"] = Ability(environment, "move", bacterium, move_predicateList, \
            move_condition, move_effect)
        bacterium.abilities["starve"] = Ability(environment, "starve", bacterium, starve_predicateList, \
            starve_condition, starve_effect)


    # create bacteria agents
    for i in range(5):
        for j in range(5):
            name = "bacterium_" + str(5 * i + j)
            bacterium = Agent(environment, name, 10 * i, 10 * j)
            bacterium.addTrait('type', 'bacteria')
            bacterium.addTrait('calories', 100)
            bacterium.addTrait('interactRange', 10)
            bacterium.size = 10
            bacterium.color = QtGui.QColor(GREEN)
            environment.agentSet.add(bacterium)

            bacterium.abilities["eat"] = Ability(environment, "eat", bacterium, eat_predicateList, \
                eat_condition, eat_effect)
            bacterium.abilities["move"] = Ability(environment, "move", bacterium, move_predicateList, \
                move_condition, move_effect)
            bacterium.abilities["divide"] = Ability(environment, "divide", bacterium, \
                divide_predicateList, divide_condition, divide_effect)
            bacterium.abilities["starve"] = Ability(environment, "starve", bacterium, starve_predicateList, \
                starve_condition, starve_effect)

    # create yogurt agents
    for i in range(20):
        for j in range(20):
            name = "yogurt_" + str(20 * i + j)
            yogurt = Agent(environment, name, 5 * i, 5 * j + 50)
            yogurt.addTrait('type', 'food')
            yogurt.addTrait('calories', 30)
            yogurt.size = 5
            yogurt.color = QtGui.QColor(PINK)
            environment.agentSet.add(yogurt)


    return

# FUNCTION GENERATE TEST CLASSES - DOG APPLE
#-------------------------------------------------------------------------------
def generateTestClasses_dogApple(environment):
    # create dog agent
    dog = Agent(environment, "dog", 5, 5)
    dog.addTrait('type', 'animal')
    dog.addTrait('calories', 500)
    dog.addTrait('eatRange', 200)
    environment.agentSet.add(dog)

    # create apple agents
    # this one is within eat range by default
    apple_close = Agent(environment, "apple_close", 100, 100)
    apple_close.addTrait('type', 'food')
    apple_close.addTrait('calories', 35)
    environment.agentSet.add(apple_close)

    # this one should not be reachable withour movement
    apple_far = Agent(environment, "apple_far", 300, 300)
    apple_far.addTrait('type', 'food')
    apple_far.addTrait('calories', 35)
    environment.agentSet.add(apple_far)

    # ability eat condition: food.type is 'food'
    #       && ((food.x - self.x)^2 + (food.y - self.y)^2)^0.5 < self.eatRange
    # !!! blocked duration predicates
    # !!! always sort predicate list before insertion into class
    # !!! THIS IS AN OUTDATED METHOD OF DEFINING ABILITIES
    eat_predicate_food_type = lambda env, sel, food: food.traits.get('type') is not None
    eat_predicate_food_x = lambda env, sel, food: food.traits.get('xCoord') is not None
    eat_predicate_food_y = lambda env, sel, food: food.traits.get('yCoord') is not None
    eat_predicate_food_calories = lambda env, sel, food: food.traits.get('calories') is not None
    eat_predicate_self_eatRange = lambda s: s.traits.get('eatRange') is not None
    eat_predicate_self_x = lambda s: s.traits.get('xCoord') is not None
    eat_predicate_self_y = lambda s: s.traits.get('yCoord') is not None
    eat_predicate_self_calories = lambda s: s.traits.get('calories') is not None
    eat_predicateList = [(1, eat_predicate_self_eatRange), \
        (1, eat_predicate_self_x), (1, eat_predicate_self_y), \
        (1, eat_predicate_self_calories), (1, eat_predicate_food_type), \
        (2, eat_predicate_food_x), (2, eat_predicate_food_y), \
        (2, eat_predicate_food_calories)]

    eat_condition = lambda targets: targets[2].traits['type'].value is 'food' \
        and ((targets[2].traits['xCoord'].value - targets[1].traits['xCoord'].value)**2 \
        + (targets[2].traits['yCoord'].value - targets[1].traits['yCoord'].value)**2)**0.5 \
        < targets[1].traits['eatRange'].value

    def eat_effect(targets, conditionality):
        if conditionality is UNCONDITIONAL:
            return

        targets[1].traits['calories'].value += targets[2].traits['calories'].value

        targets[0].agentSet.remove(targets[2])

        targets[1].blockedDuration = 10

    ability_eat = Ability(environment, "eat", dog, eat_predicateList, \
        eat_condition, eat_effect)

    dog.abilities["eat"] = ability_eat

    return

# FUNCTION EXECUTE TEST
#-------------------------------------------------------------------------------
def executeTest_dogAppleEat(environment):
    print("Testing dog and apple generation:")
    generateTestClasses(environment)
    environment.printSnapshot()
    print("...done")

    print("Testing predicate & condition casting:")
    dog_eat = environment.getAgentByName('dog').abilities['eat']
    potentialTargets = dog_eat.getPotentialTargets()
    print("...done")

    print("Testing effect & blocker casting")
    chosenTargets = dog_eat.chooseTargetSet(potentialTargets)
    dog_eat.cast(chosenTargets)
    print("...done")

    print("Result:")
    environment.printSnapshot()
