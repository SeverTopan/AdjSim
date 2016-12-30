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
import matplotlib.pyplot as plot
from constants import *
from PyQt4 import QtCore, QtGui

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

    INTELLIGENCE_NONE = 0
    INTELLIGENCE_GENETIC_ALGORITHM = 1
    INTELLIGENCE_Q_LEARNING = 2

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

# PROPERTY METHOD - SIZE
#-------------------------------------------------------------------------------
    @property
    def size(self):
        return self.traits['size'].value

    @size.setter
    def size(self, value):
        self.traits['size'].value = value
        return

# PROPERTY METHOD - TYPE
#-------------------------------------------------------------------------------
    @property
    def type(self):
        return self.traits['type'].value

    @type.setter
    def type(self, value):
        self.traits['type'].value = value
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

# PROPERTY METHOD - STYLE
#-------------------------------------------------------------------------------
    @property
    def style(self):
        return self.traits['style'].value

    @style.setter
    def style(self, value):
        self.traits['style'].value = value
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

# PROPERTY METHOD - INTELLIGENCE
#-------------------------------------------------------------------------------
    @property
    def intelligence(self):
        return self.traits['intelligence'].value

    @intelligence.setter
    def intelligence(self, value):
        self.traits['intelligence'].value = value
        return

# PROPERTY METHOD - GOALS
#-------------------------------------------------------------------------------
    @property
    def goals(self):
        return self.traits['goals'].value

    @goals.setter
    def goals(self, value):
        self.traits['goals'].value = value
        return

# PROPERTY METHOD - PERCEPTION
#-------------------------------------------------------------------------------
    @property
    def perception(self):
        return self.traits['perception'].value

    @perception.setter
    def perception(self, value):
        self.traits['perception'].value = value
        return

# PROPERTY METHOD - HISTORY
#-------------------------------------------------------------------------------
    @property
    def history(self):
        return self.traits['history'].value

    @history.setter
    def history(self, value):
        self.traits['history'].value = value
        return

# METHOD ADD TRAIT
#-------------------------------------------------------------------------------
    def addTrait(self, name, value, thoughtMutability = None):
        self.traits[name] = Trait(self.environment, name, value, thoughtMutability)

# METHOD GET TRAIT
#-------------------------------------------------------------------------------
    def getTrait(self, name):
        return self.traits.get(name).value

# METHOD EVALUATE GOALS
#-------------------------------------------------------------------------------
    def evaluateGoals(self):
        result = 0;

        for goal in self.goals:
            result += goal.evaluate()

        return result

# METHOD ADD MANDATORY TRAITS
#-------------------------------------------------------------------------------
    def addMandatoryTraits(self, x, y):
        self.addTrait('xCoord', x)
        self.addTrait('yCoord', y)
        self.addTrait('color', QtGui.QColor(BLUE_DARK))
        self.addTrait('style', QtCore.Qt.SolidPattern)
        self.addTrait('size', DEFAULT_OBJECT_RADIUS)
        self.addTrait('type', self.name)
        self.addTrait('abilities', {})
        self.addTrait('intelligence', Agent.INTELLIGENCE_NONE)
        self.addTrait('goals', [])
        self.addTrait('perception', None)
        self.addTrait('history', [])

#-------------------------------------------------------------------------------
# CLASS TARGET PREDICATE
#-------------------------------------------------------------------------------
class TargetPredicate(object):
    """docstring for TargetPredicate."""

    ENVIRONMENT = -1
    SOURCE = -2

    def __init__(self, target, predicate):
        super(TargetPredicate, self).__init__()
        self.target = target
        self.predicate = predicate

#-------------------------------------------------------------------------------
# CLASS TARGET SET
#-------------------------------------------------------------------------------
class TargetSet(object):
    """docstring for TargetSet."""
    def __init__(self, environment, source, targets = None):
        super(TargetSet, self).__init__()
        self.environment = environment
        self.source = source
        if targets == None:
            targets = []
        self.targets = targets


#-------------------------------------------------------------------------------
# CLASS ABILITY
#-------------------------------------------------------------------------------
class Ability(Resource):
    """docstring for Ability."""

# METHOD __INIT__
# * pre-parsed version
#-------------------------------------------------------------------------------
    def __init__(self, environment, name, agent, predicates, condition, effect):
        super(Ability, self).__init__(environment, name)
        self.agent = agent
        self.predicates = predicates
        self.condition = condition
        self.effect = effect

# METHOD CHECK TARGET SET COMBINATIONS
# * recursively checks all combinations of potential targets and yields valid
# * target combination sets. Function is recursive, since its complexity is
# * O(n^k), where k is the number of potential targets
#-------------------------------------------------------------------------------
    def checkTargetSetCombinations(self, potentialTargetSet, validTargetList, targetIndex = None):
        # init default argument to a mutable varible
        if targetIndex is None:
            targetIndex = TargetSet(potentialTargetSet.environment, potentialTargetSet.source, [0])

        # init current index
        currIndex = len(targetIndex.targets) - 1

        # error check
        if not potentialTargetSet:
            raise Exception('Invalid potentialTargetSet')

        for currTarget in potentialTargetSet.targets[currIndex]:
            targetIndex.targets[currIndex] = currTarget
            # if at end of recursion expansion, check condition, if not, keep
            # recursing until end is reached
            if currIndex + 1 is len(potentialTargetSet.targets):
                # at end of recursion expansion
                logging.debug("   At end of recursion expansion:")
                for target in targetIndex.targets:
                    logging.debug("     - %s", target.name)


                if self.condition(targetIndex):
                    logging.debug("   -> yielding")
                    outputTargetSet = TargetSet(targetIndex.environment, targetIndex.source, \
                        [item for item in targetIndex.targets])
                    validTargetList.append(outputTargetSet)
            else:
                # init next targetIndex Entry
                while len(targetIndex.targets) <= currIndex + 1:
                    targetIndex.targets.append(0)

                # recurse
                return self.checkTargetSetCombinations(potentialTargetSet, validTargetList, targetIndex)


# METHOD GET POTENTIAL TARGET SET
# * returns a list of sets of valid targets on which to perfrom actions
#-------------------------------------------------------------------------------
    def getPotentialTargets(self):
        potentialTargetSet = TargetSet(self.environment, self.agent)
        validTargetList = []

        # debug message
        logging.debug("Obtaining Targets: %s", self.name)

        for targetPredicate in self.predicates:
            if targetPredicate.target is TargetPredicate.ENVIRONMENT:
                # target = environment - check predicate
                if not targetPredicate.predicate(self.environment):
                    return None

            elif targetPredicate.target is TargetPredicate.SOURCE:
                # target = self - check predicate
                if not targetPredicate.predicate(self.agent):
                    return None

            else:
                newPotentialAgents = self.environment.getAgentsOnPredicate(self.agent, \
                    targetPredicate.predicate)

                # exit if no targets
                if not newPotentialAgents:
                    return None

                # so that predicates do not have to be listed in ascending order
                while len(potentialTargetSet.targets) < targetPredicate.target + 1:
                    potentialTargetSet.targets.append(None)
                potentialTargetSet.targets[targetPredicate.target] = newPotentialAgents

        logging.debug("   Potential Target Set: ")
        for targetSet in potentialTargetSet.targets:
            logging.debug("      .")
            for agent in targetSet:
                logging.debug("     %s", agent.name)
        logging.debug("      .")


        # accumulate target sets for decision if they are needed
        if len(potentialTargetSet.targets) > 0:
            self.checkTargetSetCombinations(potentialTargetSet, validTargetList)
        else:
            # only environment and self targets are required
            # only one possible target for source and environment,
            # therefore potentialTargetSet contains correct target set combination by default
            if self.condition(potentialTargetSet):
                validTargetList = [potentialTargetSet]


        if len(validTargetList) == 0:
            return None
        else:
            return validTargetList

# METHOD CHOOSE TARGET SET
# * performs decision making to determine which target set to perform an ability on
#-------------------------------------------------------------------------------
    def chooseTargetSet(self, validTargetList):
        # error check
        if not validTargetList:
            raise Exception('Empty validTargetList in method chooseTargetSet')

        # here, insert logic for higher level decision making
        # for now, return first set in the list
        return validTargetList[0]

# METHOD
#-------------------------------------------------------------------------------
    def cast(self, conditionality, targets=None):
        # error check
        if not targets and conditionality is CONDITIONAL:
            raise Exception('No targets in conditional method cast')

        # set targets in unconditional cast
        if conditionality is UNCONDITIONAL:
            targets = TargetSet(self.environment, self.agent)

        # perform target effects
        self.effect(targets, conditionality)

        return True

#-------------------------------------------------------------------------------
# CLASS HISTORY
#-------------------------------------------------------------------------------
class HistoricTimestep(object):
    """docstring for HistoricTimestep."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self):
        super(HistoricTimestep, self).__init__()
        self.abilitiesCast = []
        self.thoughtMutableTraitValues = []
        self.perceptionTuple = None
        self.goalEvaluationAchieved = 0
        self.moveScore = 0


#-------------------------------------------------------------------------------
# CLASS PERCEPTION
#-------------------------------------------------------------------------------
class Perception(object):
    """docstring for Perception."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, evaluator):
        super(Perception, self).__init__()
        self.evaluator = evaluator

# METHOD evaluate
# * return list of percieved values
#-------------------------------------------------------------------------------
    def evaluate(self, source, agentSet):
        return self.evaluator(source, agentSet)


#-------------------------------------------------------------------------------
# CLASS GOAL
#-------------------------------------------------------------------------------
class Goal(object):
    """docstring for Goal."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, agent, traitName, evaluationFunction):
        super(Goal, self).__init__()
        self.trait = agent.traits[traitName]
        self.evaluationFunction = evaluationFunction

# METHOD evaluate
# * return weighted goal result
#-------------------------------------------------------------------------------
    def evaluate(self):
        return self.evaluationFunction(self.trait)

#-------------------------------------------------------------------------------
# CLASS THOUGHT MUTABILITY
#-------------------------------------------------------------------------------
class ThoughtMutability(object):
    """docstring for ThoughtMutability."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, acceptableValues):
        super(ThoughtMutability, self).__init__()
        # in future, accept continuous variables here
        self.acceptableValues = acceptableValues

#-------------------------------------------------------------------------------
# CLASS TRAIT
#-------------------------------------------------------------------------------
class Trait(Resource):
    """docstring for Trait."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, name, value, thoughtMutability = None):
        super(Trait, self).__init__(environment, name)
        self.value = value
        self.thoughtMutability = thoughtMutability

        # error check thought mutability types
        if thoughtMutability and type(thoughtMutability) is not ThoughtMutability:
            raise Exception("Incorrect ThoughtMutability object type")

#-------------------------------------------------------------------------------
# CLASS ANALYSIS INDEX
#-------------------------------------------------------------------------------
class AnalysisIndex(object):
    """docstring for AnalysisIndex."""

    ACCUMULATE_AGENTS = 1
    # in future, allow for different index types here

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, traitName, indexType):
        super(AnalysisIndex, self).__init__()
        self.environment = environment
        self.traitName = traitName
        self.indexType = indexType
        self.index = {}

# METHOD LOG TIMESTEP VALUES
#-------------------------------------------------------------------------------
    def logTimestepValues(self, timestep):
        if self.indexType is AnalysisIndex.ACCUMULATE_AGENTS:
            for agent in self.environment.agentSet:
                trait = agent.traits.get(self.traitName)

                # continue if trait index we are looking for is not found
                if not trait:
                    continue

                # init index list if new
                indexList = self.index.get(trait.value)
                if not indexList:
                    self.index[trait.value] = []
                    indexList = self.index[trait.value]

                # extend the list up until the current timestep,
                # no agents were detected hence append 0
                while len(indexList) <= timestep:
                    indexList.append(0)

                # append current timestep
                indexList[timestep] += 1

# METHOD LOG TIMESTEP VALUES
#-------------------------------------------------------------------------------
    def plot(self):
        if self.indexType is AnalysisIndex.ACCUMULATE_AGENTS:
            for key, val in self.index.items():
                plot.plot(val, label=key)

            plot.legend()
            plot.show()


#-------------------------------------------------------------------------------
# CLASS Q LEARNING
# * static container class for q learning related constants
#-------------------------------------------------------------------------------
class QLearning(object):
    """docstring for QLearning."""

    GAMMA = 0.1

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self):
        super(QLearning, self).__init__()

# METHOD EVALUATE GAMMA
#-------------------------------------------------------------------------------
    @staticmethod
    def evaluateDiscountFactor(depth):
        return QLearning.GAMMA**depth

# METHOD EVALUATE BEST MOVES
#-------------------------------------------------------------------------------
    @staticmethod
    def evaluateBestMoves(historyBank, bestMoveDict):
        for agentType, agentHistoryArray in historyBank.items():
            for agentHistory in agentHistoryArray:
                for historicTimestep in agentHistory:
                    bestMove = bestMoveDict.get(historicTimestep.perceptionTuple)

                    if not bestMove or bestMove.moveScore < historicTimestep.moveScore:
                        bestMoveDict[historicTimestep.perceptionTuple] = historicTimestep

#-------------------------------------------------------------------------------
# CLASS ENVIRONMENT
#-------------------------------------------------------------------------------
class Environment(Agent):
    """docstring for Environment."""

    SIMULATION_TYPE_TRAIN = 0
    SIMULATION_TYPE_TEST = 1

    simulationType = SIMULATION_TYPE_TRAIN

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self):
        super(Environment, self).__init__(self, "environment")
        self.addTrait('agentSet', {self})
        self.time = 0
        self.prevStepAnimationStart = time.time()

        # initialize default indices
        typeIndex = AnalysisIndex(self, 'type', AnalysisIndex.ACCUMULATE_AGENTS)
        self.addTrait('indices', {typeIndex})

        # initialize q learning matrix for intelligent agents
        self.addTrait('bestMoveDict', {})
        self.addTrait('historyBank', {})


# PROPERTY METHOD - AGENTSET
#-------------------------------------------------------------------------------
    @property
    def agentSet(self):
        return self.traits['agentSet'].value

    @agentSet.setter
    def agentSet(self, value):
        self.traits['agentSet'].value = value
        return

# PROPERTY METHOD - INDICES
#-------------------------------------------------------------------------------
    @property
    def indices(self):
        return self.traits['indices'].value

    @indices.setter
    def indices(self, value):
        self.traits['indices'].value = value
        return

# PROPERTY METHOD - AGENT TYPE Q MATRIX
#-------------------------------------------------------------------------------
    @property
    def bestMoveDict(self):
        return self.traits['bestMoveDict'].value

    @bestMoveDict.setter
    def bestMoveDict(self, value):
        self.traits['bestMoveDict'].value = value
        return

# PROPERTY METHOD - HISTORY BANK
#-------------------------------------------------------------------------------
    @property
    def historyBank(self):
        return self.traits['historyBank'].value

    @historyBank.setter
    def historyBank(self, value):
        self.traits['historyBank'].value = value
        return

# METHOD BANK HISTORY
#-------------------------------------------------------------------------------
    def bankHistory(self, agent):
        if agent.history:
            historyBank = self.historyBank.get(agent.type)

            if not historyBank:
                self.historyBank[agent.type] = [agent.history]
            else:
                historyBank.append(agent.history)

# METHOD REMOVE AGENT
#-------------------------------------------------------------------------------
    def removeAgent(self, agent):
        # store history in historyBank for later evaluation if training
        if Environment.simulationType == Environment.SIMULATION_TYPE_TRAIN:
            self.bankHistory(agent)

        self.agentSet.remove(agent)

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
    def executeAbilities(self, agent=None):
        if not agent:
            agent = self

        # delegate ability cast call based on agent intelligence type
        if agent.intelligence == Agent.INTELLIGENCE_NONE:
            return self.executeAbilities_intelligenceNone(agent)
        elif agent.intelligence == Agent.INTELLIGENCE_Q_LEARNING:
            return self.executeAbilities_intelligenceQLearning(agent)
        else:
            raise Exception("Unidentified agent intelligence type")
            return

# METHOD EXECUTE ABILITIES - Q LEARNING AGENT INTELLIGENCE
#-------------------------------------------------------------------------------
    def executeAbilities_intelligenceQLearning(self, agent):

        # error check
        if not agent.perception:
            raise Exception("Q learning for agent without perception")
        if not agent.goals:
            raise Exception("Q learning for agent without goals")

        # init newest history log frame
        agent.history.append(HistoricTimestep())

        # init type based best move dict if not already present
        if not self.bestMoveDict.get(agent.type):
            self.bestMoveDict[agent.type] = {}

        # obtain agent perception information
        currentPerceptionTuple = tuple(agent.perception.evaluate(agent, self.agentSet))

        # perform actions:
        # testing mode
        if Environment.simulationType == Environment.SIMULATION_TYPE_TEST:
            bestMove = self.bestMoveDict[agent.type].get(currentPerceptionTuple)
            if not bestMove:
                self.executeAbilities_intelligenceNone(agent)
            else:
                print('best move ability execution not implemented')
        # training mode
        elif Environment.simulationType == Environment.SIMULATION_TYPE_TRAIN:
            self.executeAbilities_intelligenceNone(agent, logHistory=True)

            # evaluate agent goal attainment value
            goalValue = agent.evaluateGoals()
            agent.history[-1].goalEvaluationAchieved = goalValue
            agent.history[-1].perceptionTuple = currentPerceptionTuple

            for index, historicTimestep in enumerate(agent.history[-10:]):
                historicTimestep.goalEvaluationAchieved += \
                    QLearning.evaluateDiscountFactor(len(agent.history) - index) * goalValue

        else:
            raise Exception('Unknown Environment Simulation Type')


# METHOD EXECUTE ABILITIES - NO AGENT INTELLIGENCE
#-------------------------------------------------------------------------------
    def executeAbilities_intelligenceNone(self, agent, logHistory=False):

        # repeatedly cast abilities until no more abilities are cast
        oneOrMoreAbilitiesCast = True
        while oneOrMoreAbilitiesCast:
            oneOrMoreAbilitiesCast = False

            # shuffle abilities to achieve random sequences
            # * this is a temporary substitute for the lack of agent decisionmaking
            # * infrastructure. It ensures that abilites like moveUp and moveDown
            # * will be called in random order
            shuffledAbilities = list(agent.abilities.values())
            random.shuffle(shuffledAbilities)
            for ability in shuffledAbilities:
                # abort if blocked or non-existent
                if ability.blockedDuration > 0 or agent.blockedDuration > 0:
                    continue

                potentialTargets = ability.getPotentialTargets()
                if not potentialTargets:
                    ability.cast(UNCONDITIONAL)
                    continue

                chosenTargets = ability.chooseTargetSet(potentialTargets)
                if not chosenTargets:
                    # this should never occur until the decsion module is implemented
                    raise Exception("Chosen Targets not selected properly")
                    continue

                logging.debug("%s casting: %s", agent.name, ability.name)

                # random choice of thought mutable trait values
                for trait in agent.traits.values():
                    if trait.thoughtMutability:
                        trait.value = random.choice(trait.thoughtMutability.acceptableValues)

                ability.cast(CONDITIONAL, chosenTargets)
                oneOrMoreAbilitiesCast = True

                # log history
                if logHistory:
                    agent.history[-1].abilitiesCast.append(ability.name)
                    agent.history[-1].thoughtMutableTraitValues.append( \
                        [t.value for t in agent.traits.values() if t.thoughtMutability])


# METHOD EXECUTE ALL AGENT ABILITIES
#-------------------------------------------------------------------------------
    def executeAllAgentAbilities(self):
        # cast abilities
        for agent in self.agentSet.copy():
            # currently, the environment abilities will only be cast once after all
            # agent abilities are complete
            if agent == self:
                continue

            self.executeAbilities(agent)

        # cast environment abilities
        self.executeAbilities()

# METHOD PLOT INDICES
#-------------------------------------------------------------------------------
    def plotIndices(self):
        for index in self.indices:
            index.plot()

# METHOD UPDATE INDICES
#-------------------------------------------------------------------------------
    def logIndices(self, timeStep):
        for index in self.indices:
            index.logTimestepValues(timeStep)

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
    def getAgentsOnPredicate(self, callingAgent, predicate):
        targetSet = set()

        for agent in self.agentSet:
            # abilities at this point can be cast onto themselves
            if predicate(self, callingAgent, agent):
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
            print("Timestep: ", timeStep)

            # perform agent operations
            self.logIndices(timeStep)
            self.executeAllAgentAbilities()
            self.executeTimestep()

            # wait for animaiton if graphics are intialized
            if thread:
                print(time.time() - self.prevStepAnimationStart)
                thread.updateSemaphore.acquire(1)
                thread.emit(thread.signal, self.agentSet.copy())
                self.prevStepAnimationStart = time.time()

        # log best moves given training simulation
        if Environment.simulationType == Environment.SIMULATION_TYPE_TRAIN:
            print('logging best moves...')

            # bank
            for agent in self.agentSet:
                self.bankHistory(agent)

            # evaluate
            QLearning.evaluateBestMoves(self.historyBank, self.bestMoveDict)

            # debug printing of best moves
            for perception, bestMove in self.bestMoveDict.items():
                print(perception, " : ", bestMove)

        # log last index entry and plot
        self.logIndices(numTimesteps)
        self.plotIndices()

        # print footer
        print("...Simulation Complete")
        # self.environment.printSnapshot()
