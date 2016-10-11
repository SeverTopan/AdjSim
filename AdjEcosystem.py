#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# * A Flexible framework on top of which to simulate the activity of an
# * 'ecosystem'.
# * Enivronment is set up via a configuration script at the beginning of each
# * simulation that sets cycle schedules, resource locations, etc.
#
# Deisgned and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import sys
import re
import inspect
import random

#-------------------------------------------------------------------------------
# CLASS RESOURCE
#-------------------------------------------------------------------------------
class Resource(object):
    """docstring for Resource."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, name):
        self.environment = environment
        self.name = name
        self.blockedDuration = 0

#-------------------------------------------------------------------------------
# CLASS AGENT
#-------------------------------------------------------------------------------
class Agent(Resource):
    """docstring for Agent."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, name, x = 0, y = 0):
        super(Agent, self).__init__(environment, name)
        self.abilities = {}
        self.traits = {}
        self.addMandatoryTraits(x, y)

# METHOD ADD TRAIT
#-------------------------------------------------------------------------------
    def addTrait(self, name, value):
        self.traits[name] = Trait(self.environment, name, value)


# METHOD ADD MANDATORY TRAITS
#-------------------------------------------------------------------------------
    def addMandatoryTraits(self, x, y):
        self.addTrait('exists', True)
        self.addTrait('xCoord', x)
        self.addTrait('yCoord', y)

#-------------------------------------------------------------------------------
# CLASS ABILITY
#-------------------------------------------------------------------------------
class Ability(Resource):
    """docstring for Ability."""

# METHOD __INIT__
# * pre-parsed version
#-------------------------------------------------------------------------------
    def __init__(self, environment, name, agent, predicates, condition, effects, blockers):
        super(Ability, self).__init__(environment, name)
        self.agent = agent
        self.predicates = predicates
        self.condition = condition
        self.effects = effects
        self.blockers = blockers

# METHOD CHECK TARGET SET COMBINATIONS
# * recursively checks all combinations of potential targets and yields valid
# * target combination sets. Function is recursive, since its complexity is
# * O(n^k), where k is the number of potential targets
#-------------------------------------------------------------------------------
    def checkTargetSetCombinations(self, potentialTargetSet, validTargetSet, targetIndex = [0]):
        currIndex = len(targetIndex) - 1

        # error check
        if len(potentialTargetSet) == 0:
            raise Exception('Invalid potentialTargetSet')

        for currTarget in potentialTargetSet[currIndex]:
            targetIndex[currIndex] = currTarget
            # if at end of recursion expansion, check condition, if not, keep
            # recursing until end is reached
            if currIndex + 1 == len(potentialTargetSet):
                print("   At end of recursion expansion:")
                for target in targetIndex:
                    print("     ", target.name)

                if self.condition(targetIndex):
                    print('   -> yielding')
                    validTargetSet.append(targetIndex)
            else:
                # init next targetIndex Entry
                if len(targetIndex) == currIndex + 1:
                    targetIndex.append(0)
                # recurse
                return self.checkTargetSetCombinations(potentialTargetSet, validTargetSet, targetIndex)

        # exit condition
        if currIndex + 1 == len(potentialTargetSet):
            return

# METHOD GET POTENTIAL TARGET SET
# * returns a list of sets of valid targets on which to perfrom actions
#-------------------------------------------------------------------------------
    def getPotentialTargets(self):
        potentialTargetSet = []
        validTargetSet = []

        for target, predicate in self.predicates:
            if target == 0:
                # target = self - check predicate
                if predicate(self.agent):
                    # add list entry if not done before
                    if not potentialTargetSet:
                        potentialTargetSet.append({self.agent})
                else:
                    return None

            else:
                newPotentialAgents = self.environment.getAgentsOnPredicate(predicate)

                # exit if no targets
                if not newPotentialAgents:
                    return None

                # insert new potential agents into potentialTargetSet
                # !!! tuple element 0 of predictes must be in sorted order
                if len(potentialTargetSet) == target:
                    potentialTargetSet.append(newPotentialAgents)
                else:
                    potentialTargetSet[target] = \
                        potentialTargetSet[target] & newPotentialAgents

                # check if intersection yields null set
                if not potentialTargetSet[target]:
                    return None

        print("   Potential Target Set: ")
        for agentSet in potentialTargetSet:
            print("      .")
            for agent in agentSet:
                print("     ", agent.name)
        print("      .")



        # accumulate target sets for decision
        self.checkTargetSetCombinations(potentialTargetSet, validTargetSet)

        if not validTargetSet:
            return None
        else:
            return validTargetSet

# METHOD CHOOSE TARGET SET
# * performs decision making to determine which target set to perform an ability on
#-------------------------------------------------------------------------------
    def chooseTargetSet(self, validTargetSet):
        # error check
        if not validTargetSet:
            raise Exception('Empty validTargetSet in method chooseTargetSet')

        # here, insert logic for higher level decision making
        # for now, return first set in the list
        return validTargetSet[0]

# METHOD CAST
#-------------------------------------------------------------------------------
    def cast(self, targets):

        # error check
        if not targets:
            raise Exception('No targets in method cast')

        # perform target effects
        for effect in self.effects:
            effect(targets)

        # perform target blocks
        for blocker in self.blockers:
            blocker(targets)

        return True


#-------------------------------------------------------------------------------
# CLASS TRAIT
#-------------------------------------------------------------------------------
class Trait(Resource):
    """docstring for Trait."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, name, value):
        super(Trait, self).__init__(environment, name)
        self.value = value

#-------------------------------------------------------------------------------
# CLASS ENVIRONMENT
#-------------------------------------------------------------------------------
class Environment(Agent):
    """docstring for Environment."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self):
        super(Environment, self).__init__(self, "environment")
        self.agentList = [self]
        self.time = 0

# METHOD SIMULATE
#-------------------------------------------------------------------------------
    def simulate(self, numTimesteps):
        # print header
        self.printSnapshot()
        print("Simulating: ", numTimesteps, " time steps")
        AdjEcosystem.horizontalRuler(24)

        # run simulation steps for num time steps
        for timeStep in range(numTimesteps):
            self.executeAbilities()
            self.executeTimestep()
            self.cleanupNonExistentAgents()

        # print footer
        print("...Simulation Complete")
        self.printSnapshot()

# METHOD EXECUTE TIMESTEP
#-------------------------------------------------------------------------------
    def executeTimestep(self):
        self.time += 1

        # decrement blockers
        for agent in self.agentList:
            for ability in agent.abilities.values():
                if ability.blockedDuration > 0:
                    ability.blockedDuration -= 1

            for trait in agent.traits.values():
                if trait.blockedDuration > 0:
                    trait.blockedDuration -= 1

            if agent.blockedDuration > 0:
                agent.blockedDuration -= 1

# METHOD EXECUTE ABILITIES
#-------------------------------------------------------------------------------
    def executeAbilities(self):
        for agent in self.agentList:
            for ability in agent.abilities.values():
                potentialTargets = ability.getPotentialTargets()
                if not potentialTargets:
                    continue

                chosenTargets = ability.chooseTargetSet(potentialTargets)
                if not chosenTargets:
                    continue

                ability.cast(chosenTargets)

# METHOD CLEANUP NON EXISTENT AGENTS
# * Removes all agents with their mandatory 'exists' trait set to False
# * To be used at the end of each timestep cycle
#-------------------------------------------------------------------------------
    def cleanupNonExistentAgents(self):
        for agent in self.agentList:
            if not agent.traits.get('exists').value:
                self.agentList.remove(agent)


# METHOD PRINT SNAPSHOT
# * Prints all simulation environment information
#-------------------------------------------------------------------------------
    def printSnapshot(self):
        print("Environment Snapshot:")
        print(AdjEcosystem.horizontalRuler(24))

        print("   timeStep: ", self.time)

        print("   Agents:")
        for i in range(len(self.agentList)):
            print("   ", i, ": ", self.agentList[i].name, " | ", self.agentList[i].blockedDuration)

            print("   Traits:")
            for key, val in self.agentList[i].traits.items():
                print("      ", key, ": ", val.value, " | ", val.blockedDuration)

            print("   Abilities:")
            for key, val in self.agentList[i].abilities.items():
                print("      ", key, " | ", val.blockedDuration)

# METHOD GET TRAIT RANDOM
#-------------------------------------------------------------------------------
    def getTraitRandom(self):
        selectedAgent = random.random() * len(self.agentList)
        selectedTrait = random.random() * len(selectedAgent.traits)

        return selectedAgent.traits[selectedTrait]

# METHOD GET AGENT BY NAME
#-------------------------------------------------------------------------------
    def getAgentByName(self, name):
        for agent in self.agentList:
            if agent.name == name:
                return agent

        return None

# METHOD GET TRAIT ON PREDICATE
#-------------------------------------------------------------------------------
    def getAgentsOnPredicate(self, predicate):
        agentSet = set()

        for agent in self.agentList:
            if predicate(agent):
                agentSet.add(agent)

        return agentSet

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
        self.environment.agentList.append(dog)

        # create apple agent
        apple = Agent(self.environment, "apple", 3, 3)
        apple.addTrait('type', 'food')
        apple.addTrait('calories', 35)
        self.environment.agentList.append(apple)

        # ability eat condition: food.type == 'food'
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

        eat_condition = lambda targets: targets[1].traits['type'].value == 'food' \
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


#-------------------------------------------------------------------------------
# MAIN EXECUTION SCRIPT
#-------------------------------------------------------------------------------
adjEcosystem = AdjEcosystem(sys.argv)

adjEcosystem.generateTestClasses()
adjEcosystem.environment.simulate(5)
