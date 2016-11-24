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

eat_predicateList = [(0, eat_predicate_env), \
   (1, eat_predicate_self), \
   (2, eat_predicate_food)]

eat_condition = lambda targets: targets[2].traits['type'].value is 'food' \
   and ((targets[2].traits['xCoord'].value - targets[1].traits['xCoord'].value)**2 \
   + (targets[2].traits['yCoord'].value - targets[1].traits['yCoord'].value)**2)**0.5 \
   < targets[1].traits['interactRange'].value

def eat_effect(targets, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targets[1].traits['calories'].value += targets[2].traits['calories'].value

   targets[0].agentSet.remove(targets[2])
   targets[1].blockedDuration = 1

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
move_predicateList = [(1, move_predicate_self)]

move_condition = lambda targets: targets[1].traits['calories'].value > MOVEMENT_COST

def move_effect(targets, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targets[1].traits['calories'].value -= MOVEMENT_COST

   randX = random.uniform(-1, 1)
   randY = random.uniform(-1, 1)
   absRand = (randX**2 + randY**2)**0.5
   movementMultiplier = targets[1].traits['interactRange'].value * 2

   dx = (randX / absRand) * movementMultiplier
   dy = (randY / absRand) * movementMultiplier

   targets[1].yCoord += dy
   targets[1].xCoord += dx

   targets[1].abilities['move'].blockedDuration = 1

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
starve_predicateList = [(1, starve_predicate_self)]

starve_condition = lambda targets: targets[1].traits['calories'].value <= MOVEMENT_COST

def starve_effect(targets, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targets[0].agentSet.remove(targets[1])
   targets[1].blockedDuration = 1

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

divide_predicateList = [(0, divide_predicate_env), (1, divide_predicate_self)]

divide_condition = lambda targets: targets[1].traits['calories'].value > 150

def divide_effect(targets, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targets[1].traits['calories'].value -= 75
   targets[1].blockedDuration = 2

   createBacteria(targets[0], targets[1].xCoord + 10, targets[1].yCoord)

#-------------------------------------------------------------------------------
# AGENT GENERATION FUNCTIONS
#-------------------------------------------------------------------------------

# BACTERIA CREATION FUNCTION
#-------------------------------------------------------------------------------
def createBacteria(environment, x, y):
    bacterium = Agent(environment, "bacterium", x, y)
    bacterium.addTrait('type', 'bacteria')
    bacterium.addTrait('calories', 75)
    bacterium.addTrait('interactRange', 10)
    bacterium.blockedDuration = 2
    bacterium.size = 10
    bacterium.color = QtGui.QColor(GREEN)
    environment.traits['agentSet'].value.add(bacterium)

    bacterium.abilities["divide"] = Ability(environment, "divide", bacterium, \
        divide_predicateList, divide_condition, divide_effect)
    bacterium.abilities["eat"] = Ability(environment, "eat", bacterium, eat_predicateList, \
        eat_condition, eat_effect)
    bacterium.abilities["move"] = Ability(environment, "move", bacterium, move_predicateList, \
        move_condition, move_effect)
    bacterium.abilities["starve"] = Ability(environment, "starve", bacterium, starve_predicateList, \
        starve_condition, starve_effect)

#-------------------------------------------------------------------------------
# AGENT CREATION SCRIPT
#-------------------------------------------------------------------------------

# create bacteria agents
for i in range(5):
   for j in range(5):
       createBacteria(environment, 10 * i, 10 * j)

# create yogurt agents
for i in range(20):
   for j in range(20):
       name = "yogurt   "
       yogurt = Agent(environment, name, 5 * i, 5 * j + 50)
       yogurt.addTrait('type', 'food')
       yogurt.addTrait('calories', 30)
       yogurt.size = 5
       yogurt.color = QtGui.QColor(PINK)
       environment.agentSet.add(yogurt)
