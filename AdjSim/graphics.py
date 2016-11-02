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

#-------------------------------------------------------------------------------
# CLASS ADJTHREAD
#-------------------------------------------------------------------------------
class AdjThread(QtCore.QThread):

# METHOD INIT
#-------------------------------------------------------------------------------
    def __init__(self, app):
        QtCore.QThread.__init__(self, parent=app)
        self.signal = QtCore.SIGNAL("update")
        self.environment = Environment()

# METHOD RUN
#-------------------------------------------------------------------------------
    def run(self):
        core.AdjSim.run(self.environment, self)


#-------------------------------------------------------------------------------
# CLASS AGENT ELLIPSE
#-------------------------------------------------------------------------------
class AgentEllipse(QtGui.QGraphicsEllipseItem):
    """docstring for AgentEllipse."""

# METHOD INIT
#-------------------------------------------------------------------------------
    def __init__(self, agent, scene):
        QtGui.QGraphicsEllipseItem.__init__(self, agent.xCoord, agent.yCoord, \
            agent.size, agent.size)
        self.setAcceptsHoverEvents(True)
        self.setBrush(QtGui.QBrush(agent.color, style = QtCore.Qt.SolidPattern))
        self.agent = agent
        self.oldXCoord = agent.xCoord
        self.oldYCoord = agent.yCoord

    def updatePosition(self):
        if self.agent.xCoord != self.oldXCoord or self.agent.yCoord != self.oldYCoord:
            self.moveBy(self.agent.xCoord - self.oldXCoord, self.agent.yCoord - self.oldYCoord)


# METHOD HOVER EVENT ENTER
#-------------------------------------------------------------------------------
    def hoverEnterEvent(self, event):
        print(self.agent.name)

# METHOD HOVER EVENT LEAVE
#-------------------------------------------------------------------------------
    def hoverLeaveEvent(self, event):
        print('Leave')


#-------------------------------------------------------------------------------
# CLASS ADJGRAPHICSVIEW
#-------------------------------------------------------------------------------
class AdjGraphicsView(QtGui.QGraphicsView):
    """docstring for GraphicsView."""

# METHOD init
#-------------------------------------------------------------------------------
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

        self.scene = QtGui.QGraphicsScene(-250, -250, 1000, \
            1000, self)
        self.setScene(self.scene)

        # init other member variables
        self.graphicsItems = {}

        # show
        self.show()


# METHOD UPDATE
#-------------------------------------------------------------------------------
    def update(self, agentSet):
        for agent in agentSet:
            # don't draw environment itself
            if agent.name is 'environment':
                continue

            if not self.graphicsItems.get(agent):
                # create graphics item with entrance animation
                print("creating agent ", agent.name)
                newEllipse = AgentEllipse(agent, self.scene)
                self.graphicsItems[agent] = newEllipse
                self.scene.addItem(newEllipse)

            elif not agent.exists:
                # destroy object with exit animation
                print("deleting agent ", agent.name)
                self.scene.removeItem(self.graphicsItems[agent])
                del self.graphicsItems[agent]

            else:
                self.graphicsItems[agent].updatePosition()
