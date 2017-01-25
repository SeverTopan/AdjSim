#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK - BACTERIA DEMO CASE
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
#standard
import random

# third party
from PyQt4 import QtGui, QtCore
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
        if agent == targetSet.source:
            continue

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
        if agent == targetSet.source:
            continue

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
        if agent == targetSet.source:
            continue

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
    initialCondition_blockLayingSwitchEngine = [(0,0),                          # 1st column
                                               (2,0),(2,1),                    # 2nd column
                                               (4,2),(4,3),(4,4),              # 3rd column
                                               (6,3),(6,4),(6,5),(7,4)]        # 4th column


    for coord in initialCondition_blockLayingSwitchEngine:
       createCell(environment, coord[0] * CELL_SIZE, coord[1] * CELL_SIZE)

    environment.abilities['compute'] = AdjSim.Simulation.Ability(environment, "compute", environment, \
       compute_predicateList, compute_condition, \
       compute_effect)


#-------------------------------------------------------------------------------
# MAIN FUNCTION
#-------------------------------------------------------------------------------

adjSim = AdjSim.AdjSim()
generateEnv(adjSim.environment)
adjSim.simulate(100, graphicsEnabled=True, plotIndices=True)
