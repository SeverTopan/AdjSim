#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# Deisgned and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
from environment import *

#-------------------------------------------------------------------------------
# CLASS ADJECOSYSTEM
#-------------------------------------------------------------------------------
class AdjEcosystem(object):
    """docstring for AdjEcosystem."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, argv):
        self.environment = Environment()
        AdjEcosystem.printWelcome()

# METHOD HORIZONTAL RULER
#-------------------------------------------------------------------------------
    @staticmethod
    def horizontalRuler(length):
        msg = ""
        for i in range(length):
            msg += "-"

        return msg

# METHOD PRINT WELCOME
#-------------------------------------------------------------------------------
    @staticmethod
    def printWelcome():
        welcomeMessage = "- AdjEcosystem -"

        print(AdjEcosystem.horizontalRuler(len(welcomeMessage)))
        print(welcomeMessage)
        print(AdjEcosystem.horizontalRuler(len(welcomeMessage)))

# METHOD PARSE CONFIG FILE
#-------------------------------------------------------------------------------
    def parseConfigFile(self, argv):
        if len(argv) != 2:
            print("Invalid arguments - usage: python AdjEcosystem.py configfile")
            return False

        try:
            configFile = open(argv[1])
        except:
            print("Unable to open file", argv[1])
            return False

        print("Parsing Config file...")



        configData = configFile.read()
        agentMatches = re.findall('(agent:\\n(.+\\n)+)+?', configData)

        # unfinished, will add config file parsing functionality after core
        # functionality is completely implemented

        return

# METHOD GENERATE TEST CLASSES
#-------------------------------------------------------------------------------
    def generateTestClasses(self):
        # create dog agent
        dog = Agent(self.environment, "dog", 5, 5)
        dog.addTrait('type', 'animal')
        dog.addTrait('calories', 500)
        dog.addTrait('eatRange', 5)
        self.environment.agentSet.add(dog)

        # create apple agent
        apple = Agent(self.environment, "apple", 3, 3)
        apple.addTrait('type', 'food')
        apple.addTrait('calories', 35)
        self.environment.agentSet.add(apple)

        # ability eat condition: food.type is 'food'
        #       && ((food.x - self.x)^2 + (food.y - self.y)^2)^0.5 < self.eatRange
        # !!! blocked duration predicates
        # !!! always sort predicate list before insertion into class
        def eat_predicate_food_type(food):
            return food.traits.get('type') != None
        eat_predicate_food_x = lambda food: food.traits.get('xCoord') != None
        eat_predicate_food_y = lambda food: food.traits.get('yCoord') != None
        eat_predicate_food_calories = lambda food: food.traits.get('calories') != None
        eat_predicate_self_eatRange = lambda s: s.traits.get('eatRange') != None
        eat_predicate_self_x = lambda s: s.traits.get('xCoord') != None
        eat_predicate_self_y = lambda s: s.traits.get('yCoord') != None
        eat_predicate_self_calories = lambda s: s.traits.get('calories') != None
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

        ability_eat = Ability(self.environment, "eat", dog, eat_predicateList, \
            eat_condition, eat_effectList, eat_blockerList)

        dog.abilities["eat"] = ability_eat

        return

# METHOD EXECUTE TEST
#-------------------------------------------------------------------------------
    def executeTest(self):
        print("Testing dog and apple generation:")
        self.generateTestClasses()
        self.environment.printSnapshot()
        print("...done")

        print("Testing predicate & condition casting:")
        dog_eat = self.environment.getAgentByName('dog').abilities['eat']
        potentialTargets = dog_eat.getPotentialTargets()
        print("...done")

        print("Testing effect & blocker casting")
        chosenTargets = dog_eat.chooseTargetSet(potentialTargets)
        dog_eat.cast(chosenTargets)
        print("...done")

        print("Result:")
        self.environment.printSnapshot()
