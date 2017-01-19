#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
# standard
import os
import sys
import re
import pickle

#-------------------------------------------------------------------------------
# GLOBAL MODULE VARIABLES
#-------------------------------------------------------------------------------
SIMULATION_TYPE_TRAIN = 0
SIMULATION_TYPE_TEST = 1

SIMULATION_TYPE = SIMULATION_TYPE_TEST

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
# CLASS Q LEARNING
# * static container class for q learning related Constants
#-------------------------------------------------------------------------------
class QLearning(object):
    """docstring for QLearning."""

    GAMMA = .95
    LOOKAHEAD_CAP = 50
    EPSILON_GREEDY_FACTOR = .7

    PRINT_DEBUG = False

    DEFAULT_FILE_NAME = re.sub('\.py', '.pkl', sys.argv[0])
    I_FILE_NAME = DEFAULT_FILE_NAME
    O_FILE_NAME = DEFAULT_FILE_NAME

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self):
        super(QLearning, self).__init__()

# METHOD SET FILE NAME
#-------------------------------------------------------------------------------
    @staticmethod
    def setIFileName(name):
        QLearning.I_FILE_NAME = name

# METHOD SET FILE NAME
#-------------------------------------------------------------------------------
    @staticmethod
    def setOFileName(name):
        QLearning.O_FILE_NAME = name

# METHOD SET FILE NAME
#-------------------------------------------------------------------------------
    @staticmethod
    def setIOFileName(name):
        QLearning.setIFileName(name)
        QLearning.setOFileName(name)

# METHOD EVALUATE GAMMA
#-------------------------------------------------------------------------------
    @staticmethod
    def evaluateDiscountFactor(depth):
        return QLearning.GAMMA**depth

# METHOD LOAD BEST MOVES
#-------------------------------------------------------------------------------
    @staticmethod
    def loadBestMoves(environment):
        # print ui messages
        if os.path.isfile(QLearning.I_FILE_NAME):
            print('Q Learning training data found; loading...')
        else:
            print('Q Learning training data not found.')
            return

        # check filename validity
        if not QLearning.I_FILE_NAME:
            raise Exception('invalid QLearning.I_FILE_NAME')

        # load data
        environment.bestMoveDict = pickle.load(open(QLearning.I_FILE_NAME, 'rb'))

        # ui messages
        if QLearning.PRINT_DEBUG:
            environment.printBestMoveDict()
        print('...done.')


# METHOD LOG BEST MOVES
#-------------------------------------------------------------------------------
    @staticmethod
    def logBestMoves(environment):
        print('logging best moves...')

        # bank
        for agent in environment.agentSet:
            environment.bankHistory(agent)

        # evaluate
        QLearning.evaluateBestMoves(environment.historyBank, environment.bestMoveDict)

        # rename old .pkl file into a tmp while the new file is being written (crash safety)
        TEMP_FILE_NAME = QLearning.I_FILE_NAME + '.tmp'
        if os.path.isfile(QLearning.I_FILE_NAME):
            os.rename(QLearning.I_FILE_NAME, TEMP_FILE_NAME)

        # check filename validity
        if not QLearning.O_FILE_NAME:
            raise Exception('invalid QLearning.O_FILE_NAME')

        # write to file
        pickle.dump(environment.bestMoveDict, open(QLearning.O_FILE_NAME, 'wb'), pickle.HIGHEST_PROTOCOL)

        # remove old file
        if os.path.isfile(TEMP_FILE_NAME):
            os.remove(TEMP_FILE_NAME)

        # print messages
        if QLearning.PRINT_DEBUG:
            environment.printBestMoveDict()

        print('...done.')



# METHOD EVALUATE BEST MOVES
#-------------------------------------------------------------------------------
    @staticmethod
    def evaluateBestMoves(historyBank, bestMoveDict):
        for agentType, agentHistoryArray in historyBank.items():
            for agentHistory in agentHistoryArray:
                for historicTimestep in agentHistory:
                    # debug message
                    if QLearning.PRINT_DEBUG:
                        print('scanning: ', historicTimestep.perceptionTuple, ' : ', \
                            historicTimestep.abilityCast, ' - ', \
                            historicTimestep.thoughtMutableTraitValues, ' - ', \
                            historicTimestep.moveScore, ' - ', \
                            historicTimestep.goalEvaluationAchieved)

                    # init type based best move dict if not already present
                    if not bestMoveDict.get(agentType):
                        bestMoveDict[agentType] = {}

                    # populate with best moves
                    bestMove = bestMoveDict[agentType].get(historicTimestep.perceptionTuple)

                    if not bestMove or bestMove.moveScore < historicTimestep.moveScore:
                        bestMoveDict[agentType][historicTimestep.perceptionTuple] = historicTimestep

                        # debug message
                        if QLearning.PRINT_DEBUG:
                            print('inserting.')

                    # debug message
                    if QLearning.PRINT_DEBUG and bestMove and bestMove.moveScore > historicTimestep.moveScore:
                        print('previous move better: ', bestMove.perceptionTuple, ' : ', \
                            bestMove.abilityCast, ' - ', \
                            bestMove.thoughtMutableTraitValues, ' - ', \
                            bestMove.moveScore, ' - ', \
                            bestMove.goalEvaluationAchieved)
