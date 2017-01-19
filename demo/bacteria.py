#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK - BACTERIA DEMO CASE
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import random

from PyQt4 import QtGui, QtCore

import AdjSim

#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------

MOVEMENT_COST = 5

#-------------------------------------------------------------------------------
# ABILITIES
#-------------------------------------------------------------------------------

# ABILITY - EAT
#-------------------------------------------------------------------------------
# ability eat condition: food.type is 'food'
#       && ((food.x - self.x)^2 + (food.y - self.y)^2)^0.5 < self.eatRange
# !!! predicates will be grouped together for ease of writing
# !!! always sort predicate list before insertion into class
def eat_predicate_food(env, sel, target):
   if target.traits.get('type') is not None \
       and target.xCoord < sel.xCoord + sel.traits.get('interactRange').value \
       and target.xCoord > sel.xCoord - sel.traits.get('interactRange').value \
       and target.yCoord < sel.yCoord + sel.traits.get('interactRange').value \
       and target.yCoord > sel.yCoord - sel.traits.get('interactRange').value \
       and target.traits.get('calories') is not None:
       return True
   else:
       return False

def eat_predicate_self(target):
   if target.traits.get('type') is not None \
       and target.traits.get('interactRange') is not None \
       and target.traits.get('calories') is not None \
       and target.blockedDuration is 0 \
       and target.abilities['eat'].blockedDuration is 0:
       return True
   else:
       return False

def eat_predicate_env(target):
   return True

eat_predicateList = [AdjSim.Simulation.TargetPredicate(AdjSim.Simulation.TargetPredicate.ENVIRONMENT, eat_predicate_env), \
   AdjSim.Simulation.TargetPredicate(AdjSim.Simulation.TargetPredicate.SOURCE, eat_predicate_self), \
   AdjSim.Simulation.TargetPredicate(0, eat_predicate_food)]

eat_condition = lambda targetSet: targetSet.targets[0].traits['type'].value is 'food' \
   and ((targetSet.targets[0].traits['xCoord'].value - targetSet.source.traits['xCoord'].value)**2 \
   + (targetSet.targets[0].traits['yCoord'].value - targetSet.source.traits['yCoord'].value)**2)**0.5 \
   < targetSet.source.traits['interactRange'].value

def eat_effect(targetSet, conditionality):
   if conditionality is AdjSim.Constants.UNCONDITIONAL:
       return

   targetSet.source.traits['calories'].value += targetSet.targets[0].traits['calories'].value

   targetSet.environment.removeAgent(targetSet.targets[0])
   targetSet.source.blockedDuration = 1

# ABILITY - MOVE
#-------------------------------------------------------------------------------
def move_predicate_self(target):
   if target.traits.get('type') is not None \
       and target.traits.get('interactRange') is not None \
       and target.traits.get('calories') is not None \
       and target.blockedDuration is 0 \
       and target.abilities['move'].blockedDuration is 0 \
       and target.blockedDuration is 0:
       return True
   else:
       return False
move_predicateList = [AdjSim.Simulation.TargetPredicate(AdjSim.Simulation.TargetPredicate.SOURCE, move_predicate_self)]

move_condition = lambda targetSet: targetSet.source.traits['calories'].value > MOVEMENT_COST

def move_effect(targetSet, conditionality):
   if conditionality is AdjSim.Constants.UNCONDITIONAL:
       return

   targetSet.source.traits['calories'].value -= MOVEMENT_COST

   randX = random.uniform(-1, 1)
   randY = random.uniform(-1, 1)
   absRand = (randX**2 + randY**2)**0.5
   movementMultiplier = targetSet.source.traits['interactRange'].value * 2

   dx = (randX / absRand) * movementMultiplier
   dy = (randY / absRand) * movementMultiplier

   targetSet.source.yCoord += dy
   targetSet.source.xCoord += dx

   targetSet.source.abilities['move'].blockedDuration = 1

# ABILITY - STARVE
#-------------------------------------------------------------------------------
def starve_predicate_self(target):
   if target.traits.get('type') is not None \
       and target.traits.get('interactRange') is not None \
       and target.traits.get('calories') is not None \
       and target.blockedDuration is 0:
       return True
   else:
       return False
starve_predicateList = [AdjSim.Simulation.TargetPredicate(AdjSim.Simulation.TargetPredicate.SOURCE, starve_predicate_self)]

starve_condition = lambda targetSet: targetSet.source.traits['calories'].value <= MOVEMENT_COST

def starve_effect(targetSet, conditionality):
   if conditionality is AdjSim.Constants.UNCONDITIONAL:
       return

   targetSet.environment.removeAgent(targetSet.source)
   targetSet.source.blockedDuration = 1

# ABILITY - DIVIDE
#-------------------------------------------------------------------------------
def divide_predicate_self(target):
   if target.traits.get('type') is not None \
       and target.traits.get('interactRange') is not None \
       and target.traits.get('calories') is not None \
       and target.blockedDuration is 0 \
       and target.abilities['divide'].blockedDuration is 0:
       return True
   else:
       return False

def divide_predicate_env(target):
   return True

divide_predicateList = [AdjSim.Simulation.TargetPredicate(AdjSim.Simulation.TargetPredicate.ENVIRONMENT, divide_predicate_env), \
    AdjSim.Simulation.TargetPredicate(AdjSim.Simulation.TargetPredicate.SOURCE, divide_predicate_self)]

divide_condition = lambda targetSet: targetSet.source.traits['calories'].value > 150

def divide_effect(targetSet, conditionality):
   if conditionality is AdjSim.Constants.UNCONDITIONAL:
       return

   targetSet.source.traits['calories'].value -= 75
   targetSet.source.blockedDuration = 2

   createBacteria(targetSet.environment, targetSet.source.xCoord + 10, targetSet.source.yCoord)

#-------------------------------------------------------------------------------
# AGENT GENERATION FUNCTIONS
#-------------------------------------------------------------------------------

# BACTERIA CREATION FUNCTION
#-------------------------------------------------------------------------------
def createBacteria(environment, x, y):
    bacterium = AdjSim.Simulation.Agent(environment, "bacterium", x, y)
    bacterium.addTrait('type', 'bacteria')
    bacterium.addTrait('calories', 75)
    bacterium.addTrait('interactRange', 10)
    bacterium.blockedDuration = 2
    bacterium.size = 10
    bacterium.color = QtGui.QColor(AdjSim.Constants.GREEN)
    environment.traits['agentSet'].value.add(bacterium)

    bacterium.abilities["divide"] = AdjSim.Simulation.Ability(environment, "divide", bacterium, \
        divide_predicateList, divide_condition, divide_effect)
    bacterium.abilities["eat"] = AdjSim.Simulation.Ability(environment, "eat", bacterium, eat_predicateList, \
        eat_condition, eat_effect)
    bacterium.abilities["move"] = AdjSim.Simulation.Ability(environment, "move", bacterium, move_predicateList, \
        move_condition, move_effect)
    bacterium.abilities["starve"] = AdjSim.Simulation.Ability(environment, "starve", bacterium, starve_predicateList, \
        starve_condition, starve_effect)

# FUNCTION GENERATE ENV
#-------------------------------------------------------------------------------
def generateEnv(environment):
    # create bacteria agents
    for i in range(5):
       for j in range(5):
           createBacteria(environment, 10 * i, 10 * j)

    # create yogurt agents
    for i in range(20):
       for j in range(20):
           name = "yogurt   "
           yogurt = AdjSim.Simulation.Agent(environment, name, 5 * i, 5 * j + 50)
           yogurt.addTrait('type', 'food')
           yogurt.addTrait('calories', 30)
           yogurt.size = 5
           yogurt.color = QtGui.QColor(AdjSim.Constants.PINK)
           environment.agentSet.add(yogurt)

#-------------------------------------------------------------------------------
# AGENT CREATION SCRIPT
#-------------------------------------------------------------------------------
adjSim = AdjSim.AdjSim()

adjSim.clearEnvironment()
generateEnv(adjSim.environment)
adjSim.simulate(10, graphicsEnabled=True, plotIndices=True)
