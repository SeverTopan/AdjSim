#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK - BACTERIA DEMO CASE
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
# standard
import random

# third party
from PyQt5 import QtGui, QtCore
import AdjSim

#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------

CELL_SIZE = 5

#-------------------------------------------------------------------------------
# ABILITIES
#-------------------------------------------------------------------------------


# ABILITY - COMPUTE
#-------------------------------------------------------------------------------
def compute_predicate_self(target):
   return target.abilities['compute'].blockedDuration is 0

compute_predicateList = [AdjSim.TargetPredicate(AdjSim.TargetPredicate.SOURCE, compute_predicate_self)]

compute_condition = lambda targetSet: True

def compute_effect(targetSet):
    # calculate neighbour
    globalNeighbourDict = {}

    # update globalNeighbourDict
    for agent in targetSet.source.agentSet:
        x = agent.xCoord
        y = agent.yCoord
        localNeighbourCoordList = [(x, y + CELL_SIZE),
                (x, y - CELL_SIZE),
                (x + CELL_SIZE, y),
                (x - CELL_SIZE, y),
                (x + CELL_SIZE, y + CELL_SIZE),
                (x - CELL_SIZE, y + CELL_SIZE),
                (x + CELL_SIZE, y - CELL_SIZE),
                (x - CELL_SIZE, y - CELL_SIZE)]

        for localNeighbourCoord in localNeighbourCoordList:
            globalNeighbourCount = globalNeighbourDict.get(localNeighbourCoord)
            if globalNeighbourCount:
                globalNeighbourDict[localNeighbourCoord] += 1
            else:
                globalNeighbourDict[localNeighbourCoord] = 1

    # update neighbourCount and kill overpopulated agents
    removeList = []
    for agent in targetSet.source.agentSet:
        coordTuple = (agent.xCoord, agent.yCoord)
        neighbourCount = globalNeighbourDict.get(coordTuple)

        if not neighbourCount:
            neighbourCount = 0
        else:
            del globalNeighbourDict[coordTuple]

        if neighbourCount < 2 or neighbourCount > 3:
            removeList.append(agent)

    # delete agents
    for agent in removeList:
        targetSet.source.removeAgent(agent)

    # add new agents
    for key, value in globalNeighbourDict.items():
        if value is 3:
            createCell(targetSet.source, key[0], key[1])

    targetSet.source.abilities['compute'].blockedDuration = 1

#-------------------------------------------------------------------------------
# AGENT GENERATION FUNCTIONS
#-------------------------------------------------------------------------------

# CELL CREATION FUNCTION
#-------------------------------------------------------------------------------
def createCell(environment, x, y):
   cell = AdjSim.Simulation.Agent(environment, "cell", x, y)
   cell.addTrait('type', 'live_cell')
   cell.size = CELL_SIZE
   cell.color = QtGui.QColor(AdjSim.Constants.BLUE_DARK)
   environment.agentSet.add(cell)


#-------------------------------------------------------------------------------
# AGENT CREATION SCRIPT
#-------------------------------------------------------------------------------
def generateEnv(environment):
    # creation script
    initialCondition_gosperGliderGun = [(0,0),(1,0),(1,1),(0,1),                                            # left-most block
                                       (10,0),(10,1),(10,-1),(11,2),(11,-2),(12,3),(12,-3),(13,3),(13,-3), # curve on left
                                       (14,0),(15,2),(15,-2),(16,1),(16,-1),(16,0),(17,0),                 # 'play button' on left
                                       (20,1),(20,2),(20,3),(21,1),(21,2),(21,3),(22,0),(22,4),            # 2x3 + 2 on right
                                       (24,-1),(24,0),(24,4),(24,5),                                       # trailing 'winglets' on right
                                       (34,2),(34,3),(35,2),(35,3)]                                        # right-most block

    for coord in initialCondition_gosperGliderGun:
       createCell(environment, coord[0] * CELL_SIZE, coord[1] * CELL_SIZE)

    environment.abilities['compute'] = AdjSim.Simulation.Ability(environment, "compute", environment, \
       compute_predicateList, compute_condition, \
       compute_effect)

#-------------------------------------------------------------------------------
# MAIN FUNCTION
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    adjSim = AdjSim.AdjSim()
    generateEnv(adjSim.environment)
    adjSim.simulate(100, graphicsEnabled=True, plotIndices=True)
