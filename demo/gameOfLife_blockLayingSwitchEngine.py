#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK - BACTERIA DEMO CASE
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import random
from environment import *
from constants import *
from PyQt4 import QtGui, QtCore

#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------

CELL_SIZE = 5

#-------------------------------------------------------------------------------
# ABILITIES
#-------------------------------------------------------------------------------


# ABILITY - CALCULATE NEIGHBOURS
#-------------------------------------------------------------------------------
# function calculateNeighbours
# !!! predicates will be grouped together for ease of writing
# !!! always sort predicate list before insertion into class
def calculateNeighbours_predicate_self(target):
   return target.abilities['calculateNeighbours'].blockedDuration is 0

calculateNeighbours_predicateList = [TargetPredicate(TargetPredicate.SOURCE, calculateNeighbours_predicate_self)]

calculateNeighbours_condition = lambda targetSet: True

def calculateNeighbours_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   x = targetSet.source.xCoord
   y = targetSet.source.yCoord

   neighbourSet = set()
   possibleNeighbourSet = {(x, y + CELL_SIZE),
                   (x, y - CELL_SIZE),
                   (x + CELL_SIZE, y),
                   (x - CELL_SIZE, y),
                   (x + CELL_SIZE, y + CELL_SIZE),
                   (x - CELL_SIZE, y + CELL_SIZE),
                   (x + CELL_SIZE, y - CELL_SIZE),
                   (x - CELL_SIZE, y - CELL_SIZE)}


   # scan for adjacent agents and store into neighbourSet set
   for agent in targetSet.environment.agentSet:
       # ignore environment and self
       if agent is targetSet.environment or agent is targetSet.source:
           continue

       # check bounding boxes
       if agent.xCoord > x + CELL_SIZE or agent.xCoord < x - CELL_SIZE \
           or agent.yCoord > y + CELL_SIZE or agent.yCoord < y - CELL_SIZE:
           continue

       for targetX, targetY in possibleNeighbourSet:
           if agent.xCoord == targetX and agent.yCoord == targetY:
               neighbourSet.add((agent.xCoord, agent.yCoord));

   # record empty agents within agentSet
   emptyNeighbourSet = possibleNeighbourSet - neighbourSet

   for item in emptyNeighbourSet:
       if targetSet.environment.traits['emptyNeighboursDict'].value.get(item) is None:
           targetSet.environment.traits['emptyNeighboursDict'].value[item] = 1
       else:
           targetSet.environment.traits['emptyNeighboursDict'].value[item] += 1

   # record num neighbours
   targetSet.source.traits['numNeighbours'].value = len(neighbourSet)

   targetSet.source.abilities['calculateNeighbours'].blockedDuration = 1


# ABILITY - ADD NEW
#-------------------------------------------------------------------------------
# !!! predicates will be grouped toget\er for ease of writing
# !!! always sort predicate list before insertion into class
def addNewAgents_predicate_self(target):
   return target.abilities['addNewAgents'].blockedDuration is 0

addNewAgents_predicateList = [TargetPredicate(TargetPredicate.SOURCE, addNewAgents_predicate_self)]

addNewAgents_condition = lambda targetSet: True

def addNewAgents_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   # delete agents
   removeList = []

   for agent in targetSet.source.agentSet:
       if agent is not targetSet.source \
           and agent.traits['numNeighbours'].value != 2 \
           and agent.traits['numNeighbours'].value != 3:
           removeList.append(agent)

   for agent in removeList:
       targetSet.source.removeAgent(agent)


   # add new agents
   emptyNeighboursDict = targetSet.environment.traits['emptyNeighboursDict'].value
   for key, value in emptyNeighboursDict.items():
       if value is 3:
           createCell(targetSet.source, key[0], key[1])

   emptyNeighboursDict.clear()

   targetSet.source.abilities['addNewAgents'].blockedDuration = 1

#-------------------------------------------------------------------------------
# AGENT GENERATION FUNCTIONS
#-------------------------------------------------------------------------------

# CELL CREATION FUNCTION
#-------------------------------------------------------------------------------
def createCell(environment, x, y):
   cell = Agent(environment, "cell", x, y)
   cell.addTrait('type', 'live_cell')
   cell.addTrait('numNeighbours', 0)
   cell.size = CELL_SIZE
   cell.color = QtGui.QColor(BLUE_DARK)
   environment.agentSet.add(cell)

   cell.abilities["calculateNeighbours"] = Ability(environment, "calculateNeighbours", cell, \
       calculateNeighbours_predicateList, calculateNeighbours_condition, \
       calculateNeighbours_effect)

#-------------------------------------------------------------------------------
# AGENT CREATION SCRIPT
#-------------------------------------------------------------------------------

# creation script
initialCondition_blockLayingSwitchEngine = [(0,0),                          # 1st column
                                           (2,0),(2,1),                    # 2nd column
                                           (4,2),(4,3),(4,4),              # 3rd column
                                           (6,3),(6,4),(6,5),(7,4)]        # 4th column


for coord in initialCondition_blockLayingSwitchEngine:
   createCell(environment, coord[0] * CELL_SIZE, coord[1] * CELL_SIZE)

environment.addTrait('emptyNeighboursDict', {})
environment.abilities['addNewAgents'] = Ability(environment, "addNewAgents", environment, \
   addNewAgents_predicateList, addNewAgents_condition, \
   addNewAgents_effect)
