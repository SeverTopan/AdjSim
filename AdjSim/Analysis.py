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

#-------------------------------------------------------------------------------
# CLASS ANALYSIS INDEX
#-------------------------------------------------------------------------------
class Index(object):
    """docstring for Index."""

    ACCUMULATE_AGENTS = 1
    AVERAGE_GOAL_VALUES = 2
    # in future, allow for different index types here

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, indexType, traitName=None):
        super(Index, self).__init__()
        self.environment = environment
        self.traitName = traitName
        self.indexType = indexType
        self.index = {}

        if not self.setup():
            raise Exception("Incorrect Analysis Index Setup")

# METHOD CHECK CORRECTNESS
# * checks whether the indexType - traitName optional variable combination is correct
#-------------------------------------------------------------------------------
    def setup(self):
        if self.indexType == Index.ACCUMULATE_AGENTS:
            return self.traitName != None
        elif self.indexType == Index.AVERAGE_GOAL_VALUES:
            self.index['Average Goal Values'] = []
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
                    rewardSum += agent.evaluateGoals()
                    intelligentAgentCount += 1

            # take average
            if intelligentAgentCount > 0:
                rewardSum /= intelligentAgentCount
            else:
                rewardSum = 0

            self.index['Average Goal Values'].append(rewardSum)

# METHOD LOG TIMESTEP VALUES
#-------------------------------------------------------------------------------
    def plot(self):
        for key, val in self.index.items():
            line, = pyplot.plot(val, label=key)
            line.set_antialiased(True)

        pyplot.legend()
        pyplot.show()
        pyplot.close()
