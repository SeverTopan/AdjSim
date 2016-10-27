#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import sys
import re
import inspect
import random
import copy
from constants import *

#-------------------------------------------------------------------------------
# CLASS RESOURCE
#-------------------------------------------------------------------------------
class Resource(object):
    """docstring for Resource."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, name):
        super(Resource, self).__init__()
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
        self.addTrait('color', None)
        self.addTrait('size', DEFAULT_OBJECT_RADIUS)
        self.addTrait('borderWidth', DEFAULT_OBJECT_BORDER_WIDTH)

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
        if not potentialTargetSet:
            raise Exception('Invalid potentialTargetSet')

        for currTarget in potentialTargetSet[currIndex]:
            targetIndex[currIndex] = currTarget
            # if at end of recursion expansion, check condition, if not, keep
            # recursing until end is reached
            if currIndex + 1 is len(potentialTargetSet):
                print("   At end of recursion expansion:")
                for target in targetIndex:
                    print("     ", target.name)

                if self.condition(targetIndex):
                    print('   -> yielding')
                    validTargetSet.append([item for item in targetIndex])
            else:
                # init next targetIndex Entry
                if len(targetIndex) is currIndex + 1:
                    targetIndex.append(0)
                # recurse
                return self.checkTargetSetCombinations(potentialTargetSet, validTargetSet, targetIndex)

        # exit condition
        if currIndex + 1 is len(potentialTargetSet):
            return

# METHOD GET POTENTIAL TARGET SET
# * returns a list of sets of valid targets on which to perfrom actions
#-------------------------------------------------------------------------------
    def getPotentialTargets(self):
        potentialTargetSet = []
        validTargetSet = []

        # debug message
        print("Casting ", self.name)

        for target, predicate in self.predicates:
            if target is 0:
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
                if len(potentialTargetSet) is target:
                    potentialTargetSet.append(newPotentialAgents)
                else:
                    potentialTargetSet[target] = \
                        potentialTargetSet[target] & newPotentialAgents

                # check if intersection yields null set
                if not potentialTargetSet[target]:
                    return None

        print("   Potential Target Set: ")
        for targetSet in potentialTargetSet:
            print("      .")
            for agent in targetSet:
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
        self.addTrait('agentSet', {self})
        self.time = 0

# PROPERTY METHOD - AGENTSET
#-------------------------------------------------------------------------------
    @property
    def agentSet(self):
        return self.traits['agentSet'].value

    @agentSet.setter
    def agentSet(self, value):
        self.traits['agentSet'].value = value
        return


# METHOD EXECUTE TIMESTEP
#-------------------------------------------------------------------------------
    def executeTimestep(self):
        self.time += 1

        # decrement blockers
        for agent in self.agentSet:
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
        # debug message
        print("Timestep: ", self.time)

        # cast abilities
        for agent in self.agentSet:
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
        discardSet = set()

        for agent in self.agentSet:
            # remove graphics link
            if agent.traits['exists'].value is False:
                 discardSet.add(agent)
                 # debug message
                 print("   ! Discarding ", agent.name)

        self.agentSet = self.agentSet - discardSet

# METHOD PRINT SNAPSHOT
# * Prints all simulation environment information
#-------------------------------------------------------------------------------
    def printSnapshot(self):
        print("Environment Snapshot:")
        print("  ".rjust(32, "-"))

        print("   timeStep: ", self.time)
        print(" |".rjust(32, "-"), " ----- |")

        print("   Agents:".ljust(30), "|        |")
        for agent in self.agentSet:
            print(" |".rjust(32, "-"), " ----- |")
            print((" " + agent.name).ljust(30), "| ", str(agent.blockedDuration).rjust(5), "|")

            print("   Traits:".ljust(30), "|        |")
            for key, val in agent.traits.items():
                if key is not 'agentSet':
                    print(("      " + key + ": " + str(val.value)).ljust(30), "| ", \
                        str(val.blockedDuration).rjust(5), "|")

            print("   Abilities:".ljust(30), "|        |")
            for key, val in agent.abilities.items():
                print(("      " + key).ljust(30), "| ", \
                    str(val.blockedDuration).rjust(5), "|")

        print(" |".rjust(32, "-"), " ----- |")

# METHOD GET TRAIT RANDOM
#-------------------------------------------------------------------------------
    def getTraitRandom(self):
        selectedAgent = random.random() * len(self.agentSet)
        selectedTrait = random.random() * len(selectedAgent.traits)

        return selectedAgent.traits[selectedTrait]

# METHOD GET AGENT BY NAME
#-------------------------------------------------------------------------------
    def getAgentByName(self, name):
        for agent in self.agentSet:
            if agent.name is name:
                return agent

        return None

# METHOD GET TRAIT ON PREDICATE
#-------------------------------------------------------------------------------
    def getAgentsOnPredicate(self, predicate):
        targetSet = set()

        for agent in self.agentSet:
            if predicate(agent):
                targetSet.add(agent)

        return targetSet
