#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import sys
import time
import random

import tests
from constants import *
from environment import *
import core

from PyQt4 import QtGui, QtCore


class AdjThread(QtCore.QThread):

    def __init__(self, app):
        QtCore.QThread.__init__(self, parent=app)
        self.signal = QtCore.SIGNAL("update")
        self.environment = Environment()

    def run(self):
        core.AdjSim.run(self.environment, self)

class AgentEllipse(QtGui.QGraphicsEllipseItem):
    """docstring for AgentEllipse."""

    def __init__(self, x, y, r, color):
        QtGui.QGraphicsEllipseItem.__init__(self, x, y, r, r)
        self.setAcceptsHoverEvents(True)
        self.setBrush(QtGui.QBrush(color, style = QtCore.Qt.SolidPattern))
        self.oldCoordX = x
        self.oldCoordY = y

    def hoverEnterEvent(self, event):
        print('Enter')

    def hoverLeaveEvent(self, event):
        print('Leave')

class AdjGraphicsView(QtGui.QGraphicsView):
    """docstring for GraphicsView."""

    def __init__(self, screenGeometry):
        QtGui.QGraphicsView.__init__(self)
        # set Qt properties
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setFrameShape(QtGui.QFrame.NoFrame)

        # init scene
        self.windowHeight = screenGeometry.height() - 100
        self.windowWidth = screenGeometry.width() - 100
        centerWidth = self.windowWidth / -2
        centerHeight = self.windowHeight / -2

        self.scene = QtGui.QGraphicsScene(-250, -250, 500, \
            500, self)
        self.setScene(self.scene)

        # init other member variables
        self.graphicsItems = {}

        # show
        self.show()

    def timerEvent(self, event):
         print("eyy")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            print("keypress")
            adjSim = core.AdjSim(sys.argv, self)
            tests.generateTestClasses_dogApple(adjSim.environment)
            adjSim.simulate(5)


# METHOD UPDATE
#-------------------------------------------------------------------------------
    def update(self, agentSet):
        for agent in agentSet:
            # don't draw environment itself
            if agent.name is 'environment':
                continue

            if not self.graphicsItems.get(agent):
                # create graphics item with entrance animation
                newEllipse = AgentEllipse(agent.xCoord, agent.yCoord, agent.size, agent.color)
                self.graphicsItems[agent] = newEllipse
                self.scene.addItem(newEllipse)

            elif not agent.exists:
                # destroy object with exit animation
                self.scene.removeItem(self.graphicsItems[agent])

            else:
                self.graphicsItems[agent].setPos(agent.xCoord, agent.yCoord)
