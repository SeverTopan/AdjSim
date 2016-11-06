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
        QtGui.QGraphicsEllipseItem.__init__(self, 0, 0, agent.size * 0.01, agent.size * 0.01)
        self.setAcceptsHoverEvents(True)
        self.setBrush(QtGui.QBrush(agent.color, style = QtCore.Qt.SolidPattern))
        self.agent = agent
        self.oldXCoord = agent.xCoord
        self.oldYCoord = agent.yCoord
        self.exitAnimationComplete = False;
        self.setPos(agent.xCoord, agent.yCoord)


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
        self.timeline = None
        self.animations = []

        # show
        self.show()


# METHOD UPDATE
#-------------------------------------------------------------------------------
    def update(self, agentSet):

        self.animations.clear()
        del self.timeline
        self.timeline = QtCore.QTimeLine(200)
        self.timeline.setFrameRange(0, 200)

        # delete items whose animations are complete
        for ellipse in self.graphicsItems.values():
            if ellipse.exitAnimationComplete:
                self.scene.removeItem(ellipse)

        self.graphicsItems = { key: val for key, val in self.graphicsItems.items() \
            if not val.exitAnimationComplete }

        # update agent ellipses
        for agent in agentSet:
            # don't draw environment itself
            if agent.name is 'environment':
                continue

            if not self.graphicsItems.get(agent):
                # create graphics item with entrance animation
                newEllipse = AgentEllipse(agent, self.scene)
                self.graphicsItems[agent] = newEllipse

                animation = QtGui.QGraphicsItemAnimation()
                animation.setTimeLine(self.timeline)
                animation.setItem(newEllipse)
                animation.setScaleAt(0, 1, 1)
                animation.setScaleAt(1, 100, 100)
                self.animations.append(animation)

                self.scene.addItem(newEllipse)

            elif not agent.exists:
                # destroy object with exit animation
                self.graphicsItems[agent].exitAnimationComplete = True
                animation = QtGui.QGraphicsItemAnimation()
                animation.setTimeLine(self.timeline)
                animation.setItem(self.graphicsItems[agent])
                animation.setScaleAt(1, 1, 1)
                animation.setScaleAt(0, 100, 100)
                self.animations.append(animation)

            else:
                moveX = agent.xCoord - self.graphicsItems[agent].oldXCoord
                moveY = agent.yCoord - self.graphicsItems[agent].oldYCoord

                if moveX != 0 or moveY != 0:
                    animation = QtGui.QGraphicsItemAnimation()
                    animation.setTimeLine(self.timeline)
                    animation.setItem(self.graphicsItems[agent])
                    animation.setPosAt(0, QtCore.QPointF(self.graphicsItems[agent].oldXCoord, self.graphicsItems[agent].oldYCoord))
                    animation.setPosAt(1, QtCore.QPointF(agent.xCoord, agent.yCoord))
                    # animation.setTranslationAt(1, 10, 10)
                    self.animations.append(animation)
                    # self.graphicsItems[agent].moveBy(moveX, moveY)

                    self.graphicsItems[agent].oldXCoord = agent.xCoord
                    self.graphicsItems[agent].oldYCoord = agent.yCoord

        self.timeline.start()
