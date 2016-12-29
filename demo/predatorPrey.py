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

eat_predicateList = [TargetPredicate(TargetPredicate.ENVIRONMENT, eat_predicate_env), \
   TargetPredicate(TargetPredicate.SOURCE, eat_predicate_self), \
   TargetPredicate(0, eat_predicate_food)]

eat_condition = lambda targetSet: ((targetSet.targets[0].traits['xCoord'].value - targetSet.source.traits['xCoord'].value)**2 \
   + (targetSet.targets[0].traits['yCoord'].value - targetSet.source.traits['yCoord'].value)**2)**0.5 \
   < targetSet.source.traits['interactRange'].value

def eat_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targetSet.source.traits['calories'].value += targetSet.targets[0].traits['calories'].value
   # targetSet.source.abilities['eat'].blockedDuration = 1

   # calorie upper bound
   if targetSet.source.traits['calories'].value > CALORIE_UPPER_BOUND_PREDATOR:
       targetSet.source.traits['calories'].value = CALORIE_UPPER_BOUND_PREDATOR

   targetSet.environment.removeAgent(targetSet.targets[0])

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
move_predicateList = [TargetPredicate(TargetPredicate.SOURCE, move_predicate_self)]

move_condition = lambda targetSet: targetSet.source.traits['calories'].value > MOVEMENT_COST

def move_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   randX = random.uniform(-1, 1)
   randY = random.uniform(-1, 1)
   absRand = (randX**2 + randY**2)**0.5
   movementMultiplier = targetSet.source.traits['interactRange'].value * 2

   newX = targetSet.source.xCoord + (randX / absRand) * movementMultiplier
   newY = targetSet.source.yCoord + (randY / absRand) * movementMultiplier

   if newX**2 + newY**2 < MOVEMENT_BOUND:
       targetSet.source.xCoord = newX
       targetSet.source.yCoord = newY
       targetSet.source.traits['calories'].value -= MOVEMENT_COST

   targetSet.source.abilities['move'].blockedDuration = 1

# ABILITY - STARVE
#-------------------------------------------------------------------------------
def starve_predicate_self(target):
   if target.traits.get('type') is not None \
       and target.traits.get('interactRange') is not None \
       and target.traits.get('calories') is not None:
       return True
   else:
       return False
starve_predicateList = [TargetPredicate(TargetPredicate.SOURCE, starve_predicate_self)]

starve_condition = lambda targetSet: targetSet.source.traits['calories'].value <= MOVEMENT_COST

def starve_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
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

divide_predicateList = [TargetPredicate(TargetPredicate.ENVIRONMENT, divide_predicate_env), \
    TargetPredicate(TargetPredicate.SOURCE, divide_predicate_self)]

divide_condition = lambda targetSet: targetSet.source.traits['calories'].value > targetSet.source.traits['divideThreshold'].value

def divide_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   if targetSet.source.traits['type'].value == 'predator':
       createPredator(targetSet.environment, targetSet.source.xCoord, targetSet.source.yCoord, division=True)
   else:
       createPrey(targetSet.environment, targetSet.source.xCoord, targetSet.source.yCoord, division=True)

   targetSet.source.traits['calories'].value -= targetSet.source.traits['divideCost'].value
   targetSet.source.blockedDuration = 1

# ABILITY - PHOTOSYNTHESIZE
#-------------------------------------------------------------------------------
photosynthesize_predicateList = []

photosynthesize_condition = lambda targetSet: True

def photosynthesize_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   blockingAgents = 0
   for agent in targetSet.environment.agentSet:
       if agent.xCoord > targetSet.source.xCoord - PHOTOSYNTHESIS_BLOCK_RANGE \
            and agent.xCoord < targetSet.source.xCoord + PHOTOSYNTHESIS_BLOCK_RANGE \
            and agent.yCoord > targetSet.source.yCoord - PHOTOSYNTHESIS_BLOCK_RANGE \
            and agent.yCoord < targetSet.source.yCoord + PHOTOSYNTHESIS_BLOCK_RANGE:
            blockingAgents += 1

            if blockingAgents > 2:
                targetSet.source.abilities['photosynthesize'].blockedDuration = 1
                return

   targetSet.source.traits['calories'].value += PHOTOSYNTHESIS_AMOUNT
   targetSet.source.abilities['photosynthesize'].blockedDuration = 1



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
