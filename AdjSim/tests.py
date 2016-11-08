#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
from environment import *
from constants import *

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
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('castLog_acc') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['calculateSetup'].blockedDuration is 0:
            return True
        else:
            return False

    def calculateSetup_predicate_env(target):
        return target.exists

    calculateSetup_predicateList = [(0, calculateSetup_predicate_env), \
        (1, calculateSetup_predicate_self)]


    calculateSetup_condition = lambda targets: True

    def calculateSetup_effect_setup(targets):
        targets[1].traits['xAcc'].value = 0;
        targets[1].traits['yAcc'].value = 0;

    def calculateSetup_effect_setCalculationStep(targets):
        targets[1].traits['castLog_acc'].value.clear()
    calculateSetup_effectList = [calculateSetup_effect_setup, \
        calculateSetup_effect_setCalculationStep]

    def calculateSetup_blocker(targets):
        targets[1].abilities['calculateSetup'].blockedDuration = 1
        targets[1].abilities['calculateAcc'].blockedDuration = 0
        targets[1].abilities['calculateVel'].blockedDuration = 0
    calculateSetup_blockerList = [calculateSetup_blocker]

    # ability - calculate acceleration
    # !!! predicates will be grouped together for ease of writing
    # !!! always sort predicate list before insertion into class
    def calculateAcc_predicate_target(env, sel, target):
        if target.exists \
            and target is not env \
            and target is not sel \
            and target.traits.get('type') is not None \
            and target.traits.get('mass') is not None:
            return True
        else:
            return False

    def calculateAcc_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('castLog_acc') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['calculateAcc'].blockedDuration is 0:
            return True
        else:
            return False

    def calculateAcc_predicate_env(target):
        return target.exists

    calculateAcc_predicateList = [(0, calculateAcc_predicate_env), \
        (1, calculateAcc_predicate_self), \
        (2, calculateAcc_predicate_target)]


    calculateAcc_condition = lambda targets: targets[2].traits['type'].value is 'planet' \
        and not targets[1].traits['castLog_acc'].value & {targets[2]} \
        and targets[0].traits['numPhysicsDependentAgents'].value > len(targets[1].traits['castLog_acc'].value)

    def calculateAcc_effect_modifyAcc(targets):
        xDist = (targets[2].xCoord - targets[1].xCoord) * DISTANCE_MULTIPLIER
        yDist = (targets[2].yCoord - targets[1].yCoord) * DISTANCE_MULTIPLIER
        absDist = (xDist**2 + yDist**2)**0.5
        absAcc = targets[2].traits['mass'].value * GRAV_CONSTANT / (absDist**2)

        targets[1].traits['xAcc'].value += absAcc * (xDist / absDist)
        targets[1].traits['yAcc'].value += absAcc * (yDist / absDist)


    def calculateAcc_effect_setCalculationStep(targets):
        targets[1].traits['castLog_acc'].value.add(targets[2])
    calculateAcc_effectList = [calculateAcc_effect_modifyAcc, \
        calculateAcc_effect_setCalculationStep]

    calculateAcc_blockerList = []

    # ability - calculate velocity
    # !!! predicates will be grouped together for ease of writing
    # !!! always sort predicate list before insertion into class
    def calculateVel_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['calculateVel'].blockedDuration is 0:
            return True
        else:
            return False

    def calculateVel_predicate_env(target):
        return target.exists

    calculateVel_predicateList = [(0, calculateVel_predicate_env), \
        (1, calculateVel_predicate_self)]

    calculateVel_condition = lambda targets: \
        targets[0].traits['numPhysicsDependentAgents'].value - 1 == len(targets[1].traits['castLog_acc'].value)

    def calculateVel_effect_modifyVel(targets):
        targets[1].traits['xVel'].value += targets[1].traits['xAcc'].value * TIMESTEP_LENGTH
        targets[1].traits['yVel'].value += targets[1].traits['yAcc'].value * TIMESTEP_LENGTH

        # print("yvel: ", targets[1].traits['yVel'].value)
        # print("xvel: ", targets[1].traits['xVel'].value)
        #
        # print("yacc: ", targets[1].traits['yAcc'].value)
        # print("xacc: ", targets[1].traits['xAcc'].value)
        #
        # print("ypos: ", targets[1].traits['yCoord'].value)
        # print("xpos: ", targets[1].traits['xCoord'].value)


        targets[1].xCoord += targets[1].traits['xVel'].value * TIMESTEP_LENGTH / DISTANCE_MULTIPLIER
        targets[1].yCoord += targets[1].traits['yVel'].value * TIMESTEP_LENGTH / DISTANCE_MULTIPLIER

    calculateVel_effectList = [calculateVel_effect_modifyVel]

    def calculateVel_blocker(targets):
        targets[1].abilities['calculateAcc'].blockedDuration = 2
        targets[1].abilities['calculateVel'].blockedDuration = 2
    calculateVel_blockerList = [calculateVel_blocker]

    def createPlanet(name, mass, size, color, xPos, yPos, xVel, yVel, environment):
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

        planet.abilities["calculateSetup"] = Ability(environment, "calculateSetup", planet, \
            calculateSetup_predicateList, calculateSetup_condition, calculateSetup_effectList, calculateSetup_blockerList)
        planet.abilities["calculateAcc"] = Ability(environment, "calculateAcc", planet, \
            calculateAcc_predicateList, calculateAcc_condition, calculateAcc_effectList, calculateAcc_blockerList)
        planet.abilities["calculateVel"] = Ability(environment, "calculateVel", planet, \
            calculateVel_predicateList, calculateVel_condition, calculateVel_effectList, calculateVel_blockerList)
        planet.abilities["calculateAcc"].blockedDuration = 2
        planet.abilities["calculateVel"].blockedDuration = 2

        environment.agentSet.add(planet)

    if identifier = 'earth':
        # earth/moon
        createPlanet('earth', 5.972e24, 5, QtCore.Qt.blue, 0, 0, 0.0 , 0, environment)
        createPlanet('moon', 7.3e22, 3, QtCore.Qt.red, 38, 0, 0.0, 1.02e3, environment)

        environment.addTrait('numPhysicsDependentAgents', 2)

    elif identifier = 'jupiter'
        # jupiter system
        createPlanet('jupiter', 1.898e27, 10, QtCore.Qt.blue, 0, 0, 0.0 , 0, environment)
        createPlanet('io', 8.9e22, 3, QtCore.Qt.red, 42, 0, 0.0, 17.38e3, environment)
        createPlanet('europa', 4.8e22, 3, QtCore.Qt.red, 67, 0, 0.0, 13.7e3, environment)
        createPlanet('ganymede', 1.48e23, 5, QtCore.Qt.red, 107, 0, 0.0, 10.88e3, environment)
        createPlanet('callisto', 1.08e23, 4, QtCore.Qt.red, 188, 0, 0.0, 8.21e3, environment)

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
        if target.exists \
            and target.traits.get('type') is not None \
            and target.xCoord < sel.xCoord + sel.traits.get('interactRange').value \
            and target.xCoord > sel.xCoord - sel.traits.get('interactRange').value \
            and target.yCoord < sel.yCoord + sel.traits.get('interactRange').value \
            and target.yCoord > sel.yCoord - sel.traits.get('interactRange').value \
            and target.traits.get('calories') is not None:
            return True
        else:
            return False

    def eat_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['eat'].blockedDuration is 0:
            return True
        else:
            return False

    def eat_predicate_env(target):
        return target.exists

    eat_predicateList = [(0, eat_predicate_env), \
        (1, eat_predicate_self), \
        (2, eat_predicate_food)]

    eat_condition = lambda targets: targets[2].traits['type'].value is 'food' \
        and ((targets[2].traits['xCoord'].value - targets[1].traits['xCoord'].value)**2 \
        + (targets[2].traits['yCoord'].value - targets[1].traits['yCoord'].value)**2)**0.5 \
        < targets[1].traits['interactRange'].value

    def eat_effect_addCalories(targets):
        targets[1].traits['calories'].value += targets[2].traits['calories'].value
    def eat_effect_killFood(targets):
        targets[2].traits['exists'].value = False
    eat_effectList = [eat_effect_killFood, eat_effect_addCalories]

    def eat_blocker_bacteria(targets):
        targets[1].blockedDuration = 1
    eat_blockerList = [eat_blocker_bacteria]

    # ability - moveUp
    def moveUp_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['moveUp'].blockedDuration is 0 \
            and target.blockedDuration is 0:
            return True
        else:
            return False
    moveUp_predicateList = [(1, moveUp_predicate_self)]

    moveUp_condition = lambda targets: targets[1].traits['calories'].value > MOVEMENT_COST

    def moveUp_effect_removeCalories(targets):
        targets[1].traits['calories'].value -= MOVEMENT_COST
    def moveUp_effect_move(targets):
        targets[1].yCoord += targets[1].traits['interactRange'].value * 2
    moveUp_effectList = [moveUp_effect_removeCalories, moveUp_effect_move]

    def moveUp_blocker_bacteria(targets):
        targets[1].abilities['moveLeft'].blockedDuration = 1
        targets[1].abilities['moveRight'].blockedDuration = 1
        targets[1].abilities['moveUp'].blockedDuration = 1
        targets[1].abilities['moveDown'].blockedDuration = 1
    moveUp_blockerList = [moveUp_blocker_bacteria]

    # ability - moveDown
    def moveDown_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['moveDown'].blockedDuration is 0 \
            and target.blockedDuration is 0:
            return True
        else:
            return False
    moveDown_predicateList = [(1, moveDown_predicate_self)]

    moveDown_condition = lambda targets: targets[1].traits['calories'].value > MOVEMENT_COST

    def moveDown_effect_removeCalories(targets):
        targets[1].traits['calories'].value -= MOVEMENT_COST
    def moveDown_effect_move(targets):
        targets[1].yCoord -= targets[1].traits['interactRange'].value * 2
    moveDown_effectList = [moveDown_effect_removeCalories, moveDown_effect_move]

    def moveDown_blocker_bacteria(targets):
        targets[1].abilities['moveLeft'].blockedDuration = 1
        targets[1].abilities['moveRight'].blockedDuration = 1
        targets[1].abilities['moveUp'].blockedDuration = 1
        targets[1].abilities['moveDown'].blockedDuration = 1
    moveDown_blockerList = [moveDown_blocker_bacteria]

    # ability - moveLeft
    def moveRight_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['moveRight'].blockedDuration is 0 \
            and target.blockedDuration is 0:
            return True
        else:
            return False
    moveRight_predicateList = [(1, moveRight_predicate_self)]

    moveRight_condition = lambda targets: targets[1].traits['calories'].value > MOVEMENT_COST

    def moveRight_effect_removeCalories(targets):
        targets[1].traits['calories'].value -= MOVEMENT_COST
    def moveRight_effect_move(targets):
        targets[1].xCoord += targets[1].traits['interactRange'].value * 2
    moveRight_effectList = [moveRight_effect_removeCalories, moveRight_effect_move]

    def moveRight_blocker_bacteria(targets):
        targets[1].abilities['moveLeft'].blockedDuration = 1
        targets[1].abilities['moveRight'].blockedDuration = 1
        targets[1].abilities['moveUp'].blockedDuration = 1
        targets[1].abilities['moveDown'].blockedDuration = 1
    moveRight_blockerList = [moveRight_blocker_bacteria]

    # ability - moveLeft
    def moveLeft_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['moveLeft'].blockedDuration is 0 \
            and target.blockedDuration is 0:
            return True
        else:
            return False
    moveLeft_predicateList = [(1, moveLeft_predicate_self)]

    moveLeft_condition = lambda targets: targets[1].traits['calories'].value > MOVEMENT_COST

    def moveLeft_effect_removeCalories(targets):
        targets[1].traits['calories'].value -= MOVEMENT_COST
    def moveLeft_effect_move(targets):
        targets[1].xCoord -= targets[1].traits['interactRange'].value * 2
    moveLeft_effectList = [moveLeft_effect_removeCalories, moveLeft_effect_move]

    def moveLeft_blocker_bacteria(targets):
        targets[1].abilities['moveLeft'].blockedDuration = 1
        targets[1].abilities['moveRight'].blockedDuration = 1
        targets[1].abilities['moveUp'].blockedDuration = 1
        targets[1].abilities['moveDown'].blockedDuration = 1
    moveLeft_blockerList = [moveLeft_blocker_bacteria]

    # ability - starve
    def starve_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0:
            return True
        else:
            return False
    starve_predicateList = [(1, starve_predicate_self)]

    starve_condition = lambda targets: targets[1].traits['calories'].value <= MOVEMENT_COST

    def starve_effect_kill(targets):
        targets[1].exists = False
    starve_effectList = [starve_effect_kill]

    def starve_blocker_bacteria(targets):
        targets[1].blockedDuration = 1
    starve_blockerList = [starve_blocker_bacteria]

    # ability - divide
    def divide_predicate_self(target):
        if target.exists \
            and target.traits.get('type') is not None \
            and target.traits.get('interactRange') is not None \
            and target.traits.get('calories') is not None \
            and target.blockedDuration is 0 \
            and target.abilities['divide'].blockedDuration is 0:
            return True
        else:
            return False

    def divide_predicate_env(target):
        return target.exists

    divide_predicateList = [(0, divide_predicate_env), (1, divide_predicate_self)]

    divide_condition = lambda targets: targets[1].traits['calories'].value > 150

    def divide_blocker_bacteria(targets):
        targets[1].blockedDuration = 2
    divide_blockerList = [divide_blocker_bacteria]

    def divide_effect_addCalories(targets):
        targets[1].traits['calories'].value -= 75
    def divide_effect_createChild(targets):
        bacterium = Agent(environment, "bacterium_child", targets[1].xCoord + 10, targets[1].yCoord)
        bacterium.addTrait('type', 'bacteria')
        bacterium.addTrait('calories', 75)
        bacterium.addTrait('interactRange', 10)
        bacterium.blockedDuration = 2
        bacterium.size = 10
        bacterium.color = QtCore.Qt.blue
        targets[0].traits['agentSet'].value.add(bacterium)

        bacterium.abilities["divide"] = Ability(environment, "divide", bacterium, \
            divide_predicateList, divide_condition, divide_effectList, divide_blockerList)
        bacterium.abilities["eat"] = Ability(environment, "eat", bacterium, eat_predicateList, \
            eat_condition, eat_effectList, eat_blockerList)
        bacterium.abilities["moveUp"] = Ability(environment, "moveUp", bacterium, moveUp_predicateList, \
            moveUp_condition, moveUp_effectList, moveUp_blockerList)
        bacterium.abilities["moveDown"] = Ability(environment, "moveDown", bacterium, moveDown_predicateList, \
            moveDown_condition, moveDown_effectList, moveDown_blockerList)
        bacterium.abilities["moveRight"] = Ability(environment, "moveRight", bacterium, moveRight_predicateList, \
            moveRight_condition, moveRight_effectList, moveRight_blockerList)
        bacterium.abilities["moveLeft"] = Ability(environment, "moveLeft", bacterium, moveLeft_predicateList, \
            moveLeft_condition, moveLeft_effectList, moveLeft_blockerList)
        bacterium.abilities["starve"] = Ability(environment, "starve", bacterium, starve_predicateList, \
            starve_condition, starve_effectList, starve_blockerList)

    divide_effectList = [divide_effect_createChild, divide_effect_addCalories]

    # create bacteria agents
    for i in range(5):
        for j in range(5):
            name = "bacterium_" + str(5 * i + j)
            bacterium = Agent(environment, name, 10 * i, 10 * j)
            bacterium.addTrait('type', 'bacteria')
            bacterium.addTrait('calories', 100)
            bacterium.addTrait('interactRange', 10)
            bacterium.size = 10
            bacterium.color = QtCore.Qt.green
            environment.agentSet.add(bacterium)

            # temporary prioritization hack
            bacterium.abilities["eat"] = Ability(environment, "eat", bacterium, eat_predicateList, \
                eat_condition, eat_effectList, eat_blockerList)
            bacterium.abilities["moveUp"] = Ability(environment, "moveUp", bacterium, moveUp_predicateList, \
                moveUp_condition, moveUp_effectList, moveUp_blockerList)
            bacterium.abilities["moveDown"] = Ability(environment, "moveDown", bacterium, moveDown_predicateList, \
                moveDown_condition, moveDown_effectList, moveDown_blockerList)
            bacterium.abilities["moveRight"] = Ability(environment, "moveRight", bacterium, moveRight_predicateList, \
                moveRight_condition, moveRight_effectList, moveRight_blockerList)
            bacterium.abilities["moveLeft"] = Ability(environment, "moveLeft", bacterium, moveLeft_predicateList, \
                moveLeft_condition, moveLeft_effectList, moveLeft_blockerList)
            bacterium.abilities["divide"] = Ability(environment, "divide", bacterium, \
                divide_predicateList, divide_condition, divide_effectList, divide_blockerList)
            bacterium.abilities["starve"] = Ability(environment, "starve", bacterium, starve_predicateList, \
                starve_condition, starve_effectList, starve_blockerList)

    # create yogurt agents
    for i in range(20):
        for j in range(20):
            name = "yogurt_" + str(20 * i + j)
            yogurt = Agent(environment, name, 5 * i, 5 * j + 50)
            yogurt.addTrait('type', 'food')
            yogurt.addTrait('calories', 30)
            yogurt.size = 5
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

    def eat_effect_addCalories(targets):
        targets[1].traits['calories'].value += targets[2].traits['calories'].value
    def eat_effect_killFood(targets):
        targets[2].traits['exists'].value = False
    eat_effectList = [eat_effect_killFood, eat_effect_addCalories]

    def eat_blocker_dog(targets):
        targets[1].blockedDuration = 10
    eat_blockerList = [eat_blocker_dog]

    ability_eat = Ability(environment, "eat", dog, eat_predicateList, \
        eat_condition, eat_effectList, eat_blockerList)

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
