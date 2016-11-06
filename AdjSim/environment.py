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
import logging
import time
from constants import *
from PyQt4 import QtCore

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
        self.traits = {}
        self.addMandatoryTraits(x, y)

# PROPERTY METHOD - XCOORD
#-------------------------------------------------------------------------------
    @property
    def xCoord(self):
        return self.traits['xCoord'].value

    @xCoord.setter
    def xCoord(self, value):
        self.traits['xCoord'].value = value
        return

# PROPERTY METHOD - YCOORD
#-------------------------------------------------------------------------------
    @property
    def yCoord(self):
        return self.traits['yCoord'].value

    @yCoord.setter
    def yCoord(self, value):
        self.traits['yCoord'].value = value
        return

# PROPERTY METHOD - EXISTS
#-------------------------------------------------------------------------------
    @property
    def exists(self):
        return self.traits['exists'].value

    @exists.setter
    def exists(self, value):
        self.traits['exists'].value = value
        return

# PROPERTY METHOD - SIZE
#-------------------------------------------------------------------------------
    @property
    def size(self):
        return self.traits['size'].value

    @size.setter
    def size(self, value):
        self.traits['size'].value = value
        return

# PROPERTY METHOD - COLOR
#-------------------------------------------------------------------------------
    @property
    def color(self):
        return self.traits['color'].value

    @color.setter
    def color(self, value):
        self.traits['color'].value = value
        return

# PROPERTY METHOD - ABILITIIES
#-------------------------------------------------------------------------------
    @property
    def abilities(self):
        return self.traits['abilities'].value

    @abilities.setter
    def abilities(self, value):
        self.traits['abilities'].value = value
        return

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
        self.addTrait('color', QtCore.Qt.red)
        self.addTrait('size', DEFAULT_OBJECT_RADIUS)
        self.addTrait('abilities', {})

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
    def checkTargetSetCombinations(self, potentialTargetSet, validTargetSet, targetIndex = None):
        # init default argument to a mutable varible
        if targetIndex is None:
            targetIndex = [0]

        # init current index
        currIndex = len(targetIndex) - 1

        # error check
        if not potentialTargetSet:
            raise Exception('Invalid potentialTargetSet')

        for currTarget in potentialTargetSet[currIndex]:
            targetIndex[currIndex] = currTarget
            # if at end of recursion expansion, check condition, if not, keep
            # recursing until end is reached
            if currIndex + 1 is len(potentialTargetSet):
                # at end of recursion expansion
                logging.debug("   At end of recursion expansion:")
                for target in targetIndex:
                    logging.debug("     %s", target.name)


                if self.condition(targetIndex):
                    logging.debug("   -> yielding")
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
        potentialTargetSet = [{self.environment}, {self.agent}]
        validTargetSet = []

        # debug message
        logging.debug("Obtaining Targets: %s", self.name)

        for target, predicate in self.predicates:
            if target is 0:
                # target = environment
                if not predicate(self.environment):
                    return None

            elif target is 1:
                # target = self - check predicate
                if not predicate(self.agent):
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

        logging.debug("   Potential Target Set: ")
        for targetSet in potentialTargetSet:
            logging.debug("      .")
            for agent in targetSet:
                logging.debug("     %s", agent.name)
        logging.debug("      .")


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
        self.prevStepAnimationStart = time.time()

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
        for agent in self.agentSet.copy():
            # shuffle abilities to achieve random sequences
            # * this is a temporary substitute for the lack of agent decisionmaking
            # * infrastructure. It ensures that abilites like moveUp and moveDown
            # * will be called in random order
            shuffledAbilities = list(agent.abilities.values())
            random.shuffle(shuffledAbilities)
            for ability in shuffledAbilities:
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
                 logging.debug("   ! Discarding %s", agent.name)

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
                # filter out unneeded keys
                if key is not 'agentSet' \
                    and key is not 'abilities' \
                    and key is not 'color' \
                    and key is not 'size':
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

# METHOD SIMULATE
#-------------------------------------------------------------------------------
    def simulate(self, numTimesteps, thread=None):
        # print header
        # self.printSnapshot()
        print("Simulating: ", numTimesteps, " time steps")

        # draw initial frame
        if thread:
            thread.emit(thread.signal, self.agentSet)
            time.sleep(1)

        # run simulation steps for num time steps
        for timeStep in range(numTimesteps):
            self.cleanupNonExistentAgents()
            self.executeAbilities()
            self.executeTimestep()

            # wait for animaiton if graphics are intialized
            if thread:
                print(time.time() - self.prevStepAnimationStart)
                while time.time() - self.prevStepAnimationStart < 0.2:
                    continue
                thread.emit(thread.signal, self.agentSet)
                self.prevStepAnimationStart = time.time()



        # print footer
        print("...Simulation Complete")
        # self.environment.printSnapshot()
