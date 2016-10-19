#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
from environment import *
from constants import *

# FUNCTION GENERATE TEST CLASSES - BACTERIA YOGURT
#-------------------------------------------------------------------------------
def generateTestClasses_bacteriaYogurt(environment):
    # create bacteria agents
    bacterium = Agent(environment, "bacterium", 5, 5)
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
    eat_predicate_food_type = lambda food: food.traits.get('type') is not None
    eat_predicate_food_x = lambda food: food.traits.get('xCoord') is not None
    eat_predicate_food_y = lambda food: food.traits.get('yCoord') is not None
    eat_predicate_food_calories = lambda food: food.traits.get('calories') is not None
    eat_predicate_self_eatRange = lambda s: s.traits.get('eatRange') is not None
    eat_predicate_self_x = lambda s: s.traits.get('xCoord') is not None
    eat_predicate_self_y = lambda s: s.traits.get('yCoord') is not None
    eat_predicate_self_calories = lambda s: s.traits.get('calories') is not None
    eat_predicateList = [(0, eat_predicate_self_eatRange), \
        (0, eat_predicate_self_x), (0, eat_predicate_self_y), \
        (0, eat_predicate_self_calories), (1, eat_predicate_food_type), \
        (1, eat_predicate_food_x), (1, eat_predicate_food_y), \
        (1, eat_predicate_food_calories)]

    eat_condition = lambda targets: targets[1].traits['type'].value is 'food' \
        and ((targets[1].traits['xCoord'].value - targets[0].traits['xCoord'].value)**2 \
        + (targets[1].traits['yCoord'].value - targets[0].traits['yCoord'].value)**2)**0.5 \
        < targets[0].traits['eatRange'].value

    def eat_effect_addCalories(targets):
        targets[0].traits['calories'].value += targets[1].traits['calories'].value
    def eat_effect_killFood(targets):
        targets[1].traits['exists'].value = False
    eat_effectList = [eat_effect_killFood, eat_effect_addCalories]

    def eat_blocker_dog(targets):
        targets[0].blockedDuration = 10
    eat_blockerList = [eat_blocker_dog]

    ability_eat = Ability(environment, "eat", dog, eat_predicateList, \
        eat_condition, eat_effectList, eat_blockerList)

    dog.abilities["eat"] = ability_eat

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
    eat_predicate_food_type = lambda food: food.traits.get('type') is not None
    eat_predicate_food_x = lambda food: food.traits.get('xCoord') is not None
    eat_predicate_food_y = lambda food: food.traits.get('yCoord') is not None
    eat_predicate_food_calories = lambda food: food.traits.get('calories') is not None
    eat_predicate_self_eatRange = lambda s: s.traits.get('eatRange') is not None
    eat_predicate_self_x = lambda s: s.traits.get('xCoord') is not None
    eat_predicate_self_y = lambda s: s.traits.get('yCoord') is not None
    eat_predicate_self_calories = lambda s: s.traits.get('calories') is not None
    eat_predicateList = [(0, eat_predicate_self_eatRange), \
        (0, eat_predicate_self_x), (0, eat_predicate_self_y), \
        (0, eat_predicate_self_calories), (1, eat_predicate_food_type), \
        (1, eat_predicate_food_x), (1, eat_predicate_food_y), \
        (1, eat_predicate_food_calories)]

    eat_condition = lambda targets: targets[1].traits['type'].value is 'food' \
        and ((targets[1].traits['xCoord'].value - targets[0].traits['xCoord'].value)**2 \
        + (targets[1].traits['yCoord'].value - targets[0].traits['yCoord'].value)**2)**0.5 \
        < targets[0].traits['eatRange'].value

    def eat_effect_addCalories(targets):
        targets[0].traits['calories'].value += targets[1].traits['calories'].value
    def eat_effect_killFood(targets):
        targets[1].traits['exists'].value = False
    eat_effectList = [eat_effect_killFood, eat_effect_addCalories]

    def eat_blocker_dog(targets):
        targets[0].blockedDuration = 10
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
