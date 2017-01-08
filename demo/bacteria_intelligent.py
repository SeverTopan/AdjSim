#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK - BACTERIA DEMO CASE
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

MOVEMENT_COST = 5
STARVE_COST = 2

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

       # eat only closest
       closestAgentDistance = (target.xCoord - sel.xCoord)**2 + (target.yCoord - sel.yCoord)**2
       closestAgent = target

       for agent in env.agentSet:
           if agent.type != 'food' or agent == target:
               continue

           currDist = (agent.xCoord - sel.xCoord)**2 + (agent.yCoord - sel.yCoord)**2
           if currDist < closestAgentDistance:
               closestAgentDistance = currDist
               closestAgent = agent
               return False

       return True
   else:
       return False

eat_predicateList = [TargetPredicate(0, eat_predicate_food)]

eat_condition = lambda targetSet: targetSet.targets[0].traits['type'].value is 'food' \
   and ((targetSet.targets[0].traits['xCoord'].value - targetSet.source.traits['xCoord'].value)**2 \
   + (targetSet.targets[0].traits['yCoord'].value - targetSet.source.traits['yCoord'].value)**2)**0.5 \
   < targetSet.source.traits['interactRange'].value

def eat_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targetSet.source.traits['calories'].value += targetSet.targets[0].traits['calories'].value
   targetSet.source.traits['dcal'].value += targetSet.targets[0].traits['calories'].value

   targetSet.environment.removeAgent(targetSet.targets[0])
   targetSet.source.blockedDuration = 1

# ABILITY - MOVE
#-------------------------------------------------------------------------------
def move_predicate_self(target):
   if target.abilities['move'].blockedDuration is 0:
       return True
   else:
       return False
move_predicateList = [TargetPredicate(TargetPredicate.SOURCE, move_predicate_self)]

move_condition = lambda targetSet: targetSet.source.traits['calories'].value > MOVEMENT_COST

def move_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targetSet.source.traits['calories'].value -= MOVEMENT_COST
   targetSet.source.traits['dcal'].value -= MOVEMENT_COST

   movementMultiplier = targetSet.source.traits['interactRange'].value * 2
   moveTheta = math.radians(targetSet.source.getTrait('moveTheta'))
   moveR = targetSet.source.getTrait('moveR') * movementMultiplier

   dx = math.cos(moveTheta) * moveR
   dy = math.sin(moveTheta) * moveR

   targetSet.source.yCoord += dy
   targetSet.source.xCoord += dx

   targetSet.source.abilities['move'].blockedDuration = 1

# ABILITY - STARVE
#-------------------------------------------------------------------------------
def starve_predicate_self(target):
   return True

starve_predicateList = [TargetPredicate(TargetPredicate.SOURCE, starve_predicate_self)]

starve_condition = lambda targetSet: True

def starve_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   removalSet = set()
   for agent in targetSet.source.agentSet:
       if agent.type == 'bacteria':
           agent.traits['calories'].value -= STARVE_COST
           agent.traits['dcal'].value = -STARVE_COST
           if agent.traits['calories'].value <= 0:
               removalSet.add(agent)

   for agent in removalSet:
       targetSet.source.removeAgent(agent)

   targetSet.source.abilities['starve'].blockedDuration = 1

# ABILITY - DIVIDE
#-------------------------------------------------------------------------------
def divide_predicate_self(target):
   if target.abilities['divide'].blockedDuration is 0:
       return True
   else:
       return False

def divide_predicate_env(target):
   return True

divide_predicateList = [TargetPredicate(TargetPredicate.ENVIRONMENT, divide_predicate_env), \
    TargetPredicate(TargetPredicate.SOURCE, divide_predicate_self)]

divide_condition = lambda targetSet: targetSet.source.traits['calories'].value > 150

def divide_effect(targetSet, conditionality):
   if conditionality is UNCONDITIONAL:
       return

   targetSet.source.traits['calories'].value -= 75
   targetSet.source.traits['dcal'].value -= 75
   targetSet.source.blockedDuration = 2

   createBacteria(targetSet.environment, targetSet.source.xCoord + 10, targetSet.source.yCoord)



# goal evaluation function
#-------------------------------------------------------------------------------
def goal_bacterium_evaluation(trait):
    return trait.value

# perception evaluation function
#-------------------------------------------------------------------------------
def perception_bacterium_evaluator(source, agentSet):
    closestAgentDistance = float('inf')
    closestAgent = None

    for agent in agentSet:
        if agent.type != 'food':
            continue

        currDist = (agent.xCoord - source.xCoord)**2 + (agent.yCoord - source.yCoord)**2
        if currDist < closestAgentDistance:
            closestAgentDistance = currDist
            closestAgent = agent

    if not closestAgent:
        return (0, 0)

    # handle division by 0
    if closestAgent.xCoord - source.xCoord == 0:
        theta = math.copysign(math.pi, (closestAgent.yCoord - source.yCoord))
    else:
        theta = math.atan((closestAgent.yCoord - source.yCoord)/(closestAgent.xCoord - source.xCoord))
    r = closestAgentDistance**0.5

    # state discrimination traits
    canMove = source.abilities['move'].blockedDuration > 0
    # canDivide = source.abilities['divide'].blockedDuration > 0
    canEat = source.abilities['eat'].blockedDuration > 0

    return (round(theta, 2), round(r), canMove, canEat)


#-------------------------------------------------------------------------------
# AGENT GENERATION FUNCTIONS
#-------------------------------------------------------------------------------

# BACTERIA CREATION FUNCTION
#-------------------------------------------------------------------------------
def createBacteria(environment, x, y):
    bacterium = Agent(environment, "bacterium", x, y)
    bacterium.addTrait('type', 'bacteria')
    bacterium.addTrait('calories', 75)
    bacterium.addTrait('dcal', 0)
    bacterium.addTrait('interactRange', 10)
    bacterium.intelligence = Agent.INTELLIGENCE_Q_LEARNING
    bacterium.size = 10
    bacterium.color = QtGui.QColor(GREEN)
    environment.traits['agentSet'].value.add(bacterium)

    # thought mutable movement
    bacterium.addTrait('moveTheta', 0, ThoughtMutability([x for x in range(0, 360, 20)]))
    bacterium.addTrait('moveR', 0, ThoughtMutability([y/10 for y in range(11)]))

    # bacterium.abilities["divide"] = Ability(environment, "divide", bacterium, \
    #     divide_predicateList, divide_condition, divide_effect)
    bacterium.abilities["eat"] = Ability(environment, "eat", bacterium, eat_predicateList, \
        eat_condition, eat_effect)
    bacterium.abilities["move"] = Ability(environment, "move", bacterium, move_predicateList, \
        move_condition, move_effect)


    # goals
    bacterium.goals.append(Goal(bacterium, 'dcal', goal_bacterium_evaluation))

    # perception
    bacterium.addTrait('perception', Perception(perception_bacterium_evaluator))

#-------------------------------------------------------------------------------
# AGENT CREATION SCRIPT
#-------------------------------------------------------------------------------

# create bacteria agents
for i in range(5):
   for j in range(5):
       createBacteria(environment, 10 * i, 10* j)

# create yogurt agents
for i in range(20):
   for j in range(20):
       name = "yogurt"
       yogurt = Agent(environment, name, 5 * i, 5 * j + 50)
       yogurt.addTrait('type', 'food')
       yogurt.addTrait('calories', 30)
       yogurt.size = 5
       yogurt.color = QtGui.QColor(PINK)
       environment.agentSet.add(yogurt)

# for _ in range(20):
#     createBacteria(environment, 0, 30)
# createBacteria(environment, 0, 30)

# init environment
environment.abilities["starve"] = Ability(environment, "starve", environment, \
    starve_predicateList, starve_condition, starve_effect)
