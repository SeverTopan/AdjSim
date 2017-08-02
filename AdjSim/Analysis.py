#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
# standard

# third party
from matplotlib import pyplot

# local
from . import Intelligence

#-------------------------------------------------------------------------------
# CLASS ANALYSIS INDEX
#-------------------------------------------------------------------------------
class Index(object):
    """docstring for Index."""

    ACCUMULATE_AGENTS = 1
    AVERAGE_GOAL_VALUES = 2
    INDIVIDUAL_GOAL_VALUES = 3
    AVERAGE_QLEARNING_REWARD = 4
    INDIVIDUAL_QLEARNING_REWARD = 5

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, indexType, traitName=None):
        super(Index, self).__init__()
        self.environment = environment
        self.traitName = traitName
        self.indexType = indexType
        self.showLegend = None
        self.index = {}

        if not self.setup():
            raise Exception("Incorrect Analysis Index Setup")


# METHOD APPLY Q LEARNING REWARD
#-------------------------------------------------------------------------------
    @staticmethod
    def applyQLearningRewardOnLastElement(goalEvaluationList):
        i = len(goalEvaluationList) - 1
        j = 1
        while i - j >= 0 and j < Intelligence.QLearning.LOOKAHEAD_CAP:
            goalEvaluationList[i - j] += goalEvaluationList[i] * Intelligence.QLearning.evaluateDiscountFactor(j)
            j += 1


# METHOD CHECK CORRECTNESS
# * checks whether the indexType - traitName optional variable combination is correct
#-------------------------------------------------------------------------------
    def setup(self):
        if self.indexType == Index.ACCUMULATE_AGENTS:
            self.showLegend = True
            return self.traitName != None

        elif self.indexType == Index.AVERAGE_GOAL_VALUES:
            self.showLegend = True
            self.index['Average Goal Values'] = []
            return self.traitName == None

        elif self.indexType == Index.INDIVIDUAL_GOAL_VALUES:
            self.showLegend = False
            return self.traitName == None

        elif self.indexType == Index.AVERAGE_QLEARNING_REWARD:
            self.showLegend = True
            self.index['Average QLearning Reward'] = []
            return self.traitName == None

        elif self.indexType == Index.INDIVIDUAL_QLEARNING_REWARD:
            self.showLegend = False
            return self.traitName == None


        return False


# METHOD LOG TIMESTEP VALUES
#-------------------------------------------------------------------------------
    def logValueAtTimestep(self, timestep):
        if self.indexType == Index.ACCUMULATE_AGENTS:
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

        elif self.indexType == Index.AVERAGE_GOAL_VALUES:
            rewardSum = 0
            intelligentAgentCount = 0

            # iterate over agents, accumulate
            for agent in self.environment.agentSet:
                if len(agent.goals) > 0:
                    rewardSum += agent.traits['_lastGoalEvaluation'].value
                    intelligentAgentCount += 1

            # take average
            if intelligentAgentCount > 0:
                rewardSum /= intelligentAgentCount
            else:
                rewardSum = 0

            self.index['Average Goal Values'].append(rewardSum)

        elif self.indexType == Index.INDIVIDUAL_GOAL_VALUES:
            for agent in self.environment.agentSet:
                if len(agent.goals) > 0:
                    # init index list if new
                    indexList = self.index.get(agent)
                    if not indexList:
                        self.index[agent] = []
                        indexList = self.index[agent]

                    # extend the list up until the current timestep,
                    # no agents were detected hence append 0
                    while len(indexList) <= timestep:
                        indexList.append(0)

                    # append current timestep
                    indexList[timestep] += agent.traits['_lastGoalEvaluation'].value

        elif self.indexType == Index.AVERAGE_QLEARNING_REWARD:
            rewardSum = 0
            intelligentAgentCount = 0

            # iterate over agents, accumulate
            for agent in self.environment.agentSet:
                if len(agent.goals) > 0:
                    rewardSum += agent.traits['_lastGoalEvaluation'].value
                    intelligentAgentCount += 1

            # take average
            if intelligentAgentCount > 0:
                rewardSum /= intelligentAgentCount
            else:
                rewardSum = 0

            Index.applyQLearningRewardOnLastElement(self.index['Average QLearning Reward'])
            self.index['Average QLearning Reward'].append(rewardSum)

        elif self.indexType == Index.INDIVIDUAL_QLEARNING_REWARD:
            for agent in self.environment.agentSet:
                if len(agent.goals) > 0:
                    # init index list if new
                    indexList = self.index.get(agent)
                    if not indexList:
                        self.index[agent] = []
                        indexList = self.index[agent]

                    # extend the list up until the current timestep,
                    # no agents were detected hence append 0
                    while len(indexList) <= timestep:
                        indexList.append(0)

                    # append current timestep
                    indexList[timestep] += agent.traits['_lastGoalEvaluation'].value
                    Index.applyQLearningRewardOnLastElement(self.index.get(agent))

# METHOD LOG TIMESTEP VALUES
#-------------------------------------------------------------------------------
    def plot(self):
        pyplot.style.use('ggplot')

        for key, val in self.index.items():
            line, = pyplot.plot(val, label=key)
            line.set_antialiased(True)

        if self.showLegend:
            pyplot.legend()

        pyplot.show()
        pyplot.close()
