#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK - JUPITER MOON SYSTEM
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

GRAV_CONSTANT = 6.674e-11
TIMESTEP_LENGTH = 10000
DISTANCE_MULTIPLIER = 10000000

#-------------------------------------------------------------------------------
# ABILITIES
#-------------------------------------------------------------------------------

# ABILITY - APPLY GRAVITY
#-------------------------------------------------------------------------------
applyGravity_predicateList = []

applyGravity_condition = lambda targetSet : True

def applyGravity_effect(targetSet, conditionality):
    if conditionality is UNCONDITIONAL:
        return

    # reset acceleration
    for agent in targetSet.source.agentSet:
        if agent == targetSet.source:
            continue

        agent.traits['xAcc'].value = 0
        agent.traits['yAcc'].value = 0

    # calculate new accelleration
    for baseAgent in targetSet.source.agentSet:
        if baseAgent == targetSet.source:
            continue

        for targetAgent in targetSet.source.agentSet:
            if targetAgent == targetSet.source or targetAgent == baseAgent:
                continue

            xDist = (baseAgent.xCoord - targetAgent.xCoord) * DISTANCE_MULTIPLIER
            yDist = (baseAgent.yCoord - targetAgent.yCoord) * DISTANCE_MULTIPLIER
            absDist = (xDist**2 + yDist**2)**0.5
            absAcc = baseAgent.traits['mass'].value * GRAV_CONSTANT / (absDist**2)

            targetAgent.traits['xAcc'].value += absAcc * (xDist / absDist)
            targetAgent.traits['yAcc'].value += absAcc * (yDist / absDist)


    # calculate new velocity and position
    for agent in targetSet.source.agentSet:
        if agent == targetSet.source:
            continue

        agent.traits['xVel'].value += agent.traits['xAcc'].value * TIMESTEP_LENGTH
        agent.traits['yVel'].value += agent.traits['yAcc'].value * TIMESTEP_LENGTH

        agent.xCoord += agent.traits['xVel'].value * TIMESTEP_LENGTH / DISTANCE_MULTIPLIER
        agent.yCoord += agent.traits['yVel'].value * TIMESTEP_LENGTH / DISTANCE_MULTIPLIER


    targetSet.source.abilities['applyGravity'].blockedDuration = 1

#-------------------------------------------------------------------------------
# AGENT GENERATION FUNCTIONS
#-------------------------------------------------------------------------------

# PLANET CREATION FUNCTION
#-------------------------------------------------------------------------------
def createPlanet(name, mass, size, color, xPos, yPos, xVel, yVel, environment, style = QtCore.Qt.SolidPattern):
   planet = Agent(environment, name, xPos, yPos)
   planet.addTrait('type', 'planet')
   planet.addTrait('xVel', xVel)
   planet.addTrait('yVel', yVel)
   planet.addTrait('xAcc', 0.0)
   planet.addTrait('yAcc', 0.0)
   planet.addTrait('mass', mass)
   planet.addTrait('castLog_acc', set())
   planet.size = size
   planet.color = color
   planet.style = style

   environment.agentSet.add(planet)

#-------------------------------------------------------------------------------
# AGENT CREATION SCRIPT
#-------------------------------------------------------------------------------

# jupiter system
createPlanet('jupiter', 1.898e27, 10, QtGui.QColor(ORANGE), 0, 0, 0.0 , 0, environment, QtCore.Qt.Dense1Pattern)
createPlanet('io', 8.9e22, 3, QtGui.QColor(GREY), 42, 0, 0.0, 17.38e3, environment)
createPlanet('europa', 4.8e22, 3, QtGui.QColor(BLUE_LIGHT), 67, 0, 0.0, 13.7e3, environment)
createPlanet('ganymede', 1.48e23, 5, QtGui.QColor(RED_DARK), 107, 0, 0.0, 10.88e3, environment)
createPlanet('callisto', 1.08e23, 4, QtGui.QColor(BROWN_LIGHT), 188, 0, 0.0, 8.21e3, environment)

environment.abilities["applyGravity"] = Ability(environment, "applyGravity", environment, \
    applyGravity_predicateList, applyGravity_condition, applyGravity_effect)
