#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK - PREDATOR/PREY DEMO CASE
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import random, math
from environment import *
from constants import *
from PyQt4 import QtGui, QtCore

#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------

MOVEMENT_COST = 8
PHOTOSYNTHESIS_AMOUNT = 15
PHOTOSYNTHESIS_BLOCK_RANGE = 5
MOVEMENT_BOUND = 70000
CALORIE_UPPER_BOUND_PREDATOR = 400

#-------------------------------------------------------------------------------
# ABILITIES
#-------------------------------------------------------------------------------

# ABILITY - EAT
#-------------------------------------------------------------------------------
#       && ((food.x - self.x)^2 + (food.y - self.y)^2)^0.5 < self.eatRange
# !!! predicates will be grouped together for ease of writing
# !!! always sort predicate list before insertion into class
def eat_predicate_food(env, sel, target):
   if target.traits.get('type') is not None and target.traits.get('type').value is 'prey' \
       and target.xCoord < sel.xCoord + sel.traits.get('interactRange').value \
       and target.xCoord > sel.xCoord - sel.traits.get('interactRange').value \
       and target.yCoord < sel.yCoord + sel.traits.get('interactRange').value \
       and target.yCoord > sel.yCoord - sel.traits.get('interactRange').value:
       return True
   else:
       return False

def eat_predicate_self(target):
   return True

def eat_predicate_env(target):
   return True

eat_predicateList = [(0, eat_predicate_env), \
   (1, eat_predicate_self), \
   (2, eat_predicate_food)]

eat_condition = lambda targets: ((targets[2].traits['xCoord'].value - targets[1].traits['xCoord'].value)**2 \
   + (targets[2].traits['yCoord'].value - targets[1].traits['yCoord'].value)**2)**0.5 \
   < targets[1].traits['interactRange'].value

def eat_effect(targets, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targets[1].traits['calories'].value += targets[2].traits['calories'].value
   # targets[1].abilities['eat'].blockedDuration = 1

   # calorie upper bound
   if targets[1].traits['calories'].value > CALORIE_UPPER_BOUND_PREDATOR:
       targets[1].traits['calories'].value = CALORIE_UPPER_BOUND_PREDATOR

   targets[0].agentSet.remove(targets[2])

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

   randX = random.uniform(-1, 1)
   randY = random.uniform(-1, 1)
   absRand = (randX**2 + randY**2)**0.5
   movementMultiplier = targets[1].traits['interactRange'].value * 2

   newX = targets[1].xCoord + (randX / absRand) * movementMultiplier
   newY = targets[1].yCoord + (randY / absRand) * movementMultiplier

   if newX**2 + newY**2 < MOVEMENT_BOUND:
       targets[1].xCoord = newX
       targets[1].yCoord = newY
       targets[1].traits['calories'].value -= MOVEMENT_COST

   targets[1].abilities['move'].blockedDuration = 1

# ABILITY - STARVE
#-------------------------------------------------------------------------------
def starve_predicate_self(target):
   if target.traits.get('type') is not None \
       and target.traits.get('interactRange') is not None \
       and target.traits.get('calories') is not None:
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

divide_condition = lambda targets: targets[1].traits['calories'].value > targets[1].traits['divideThreshold'].value

def divide_effect(targets, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   if targets[1].traits['type'].value == 'predator':
       createPredator(targets[0], targets[1].xCoord, targets[1].yCoord, division=True)
   else:
       createPrey(targets[0], targets[1].xCoord, targets[1].yCoord, division=True)

   targets[1].traits['calories'].value -= targets[1].traits['divideCost'].value
   targets[1].blockedDuration = 1

# ABILITY - PHOTOSYNTHESIZE
#-------------------------------------------------------------------------------
def photosynthesize_predicate_self(target):
   return True

def photosynthesize_predicate_env(target):
   return True

photosynthesize_predicateList = [(0, photosynthesize_predicate_env),
                                (1, photosynthesize_predicate_self)]

photosynthesize_condition = lambda targets: True

def photosynthesize_effect(targets, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   blockingAgents = 0
   for agent in targets[0].agentSet:
       if agent.xCoord > targets[1].xCoord - PHOTOSYNTHESIS_BLOCK_RANGE \
            and agent.xCoord < targets[1].xCoord + PHOTOSYNTHESIS_BLOCK_RANGE \
            and agent.yCoord > targets[1].yCoord - PHOTOSYNTHESIS_BLOCK_RANGE \
            and agent.yCoord < targets[1].yCoord + PHOTOSYNTHESIS_BLOCK_RANGE:
            blockingAgents += 1

            if blockingAgents > 2:
                targets[1].abilities['photosynthesize'].blockedDuration = 1
                return

   targets[1].traits['calories'].value += PHOTOSYNTHESIS_AMOUNT
   targets[1].abilities['photosynthesize'].blockedDuration = 1



#-------------------------------------------------------------------------------
# AGENT GENERATION FUNCTIONS
#-------------------------------------------------------------------------------

# PREDATOR CREATION FUNCTION
#-------------------------------------------------------------------------------
def createPredator(environment, x, y, division):
   calorieLevel = 75 if division else random.randint(50, 75)

   predator = Agent(environment, "predator", x, y)
   predator.addTrait('type', 'predator')
   predator.addTrait('calories', calorieLevel)
   predator.addTrait('interactRange', 15)
   predator.addTrait('divideThreshold', 250)
   predator.addTrait('divideCost', 125)
   predator.blockedDuration = 1
   predator.size = 10
   predator.color = QtGui.QColor(RED_DARK)
   environment.traits['agentSet'].value.add(predator)

   predator.abilities["divide"] = Ability(environment, "divide", predator, \
       divide_predicateList, divide_condition, divide_effect)
   predator.abilities["eat"] = Ability(environment, "eat", predator, eat_predicateList, \
       eat_condition, eat_effect)
   predator.abilities["move"] = Ability(environment, "move", predator, move_predicateList, \
       move_condition, move_effect)
   predator.abilities["starve"] = Ability(environment, "starve", predator, starve_predicateList, \
       starve_condition, starve_effect)

# PREY CREATION FUNCTION
#-------------------------------------------------------------------------------
def createPrey(environment, x, y, division):
   calorieLevel =  5 if division else random.randint(5, 35)

   prey = Agent(environment, "prey", x, y)
   prey.addTrait('type', 'prey')
   prey.addTrait('calories', calorieLevel)
   prey.addTrait('interactRange', 10)
   prey.addTrait('divideThreshold', 40)
   prey.addTrait('divideCost', 20)
   prey.blockedDuration = 2
   prey.size = 5
   prey.color = QtGui.QColor(BLUE_DARK)
   environment.traits['agentSet'].value.add(prey)

   prey.abilities["photosynthesize"] = Ability(environment, "photosynthesize", prey, photosynthesize_predicateList, \
       photosynthesize_condition, photosynthesize_effect)
   prey.abilities["move"] = Ability(environment, "move", prey, move_predicateList, \
       move_condition, move_effect)
   prey.abilities["divide"] = Ability(environment, "divide", prey, \
       divide_predicateList, divide_condition, divide_effect)

#-------------------------------------------------------------------------------
# AGENT CREATION SCRIPT
#-------------------------------------------------------------------------------

# obtain theta value list
thetaValues = [x*0.2 for x in range(1, 32)]

# create predator agents
SPACING = 75
for theta in thetaValues:
   for d in range(1,3):
       createPredator(environment, d*SPACING*math.cos(theta), d*SPACING*math.sin(theta), division=False)


# create prey agents
SPACING = 25
for theta in thetaValues:
   for d in range(1,10):
       createPrey(environment, d*SPACING*math.cos(theta), d*SPACING*math.sin(theta), division=False)
