#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
# standard
import sys
import time
import random

# third party
from PyQt5 import QtGui, QtCore, QtWidgets

# local
from . import Simulation
from . import Analysis

#-------------------------------------------------------------------------------
# CLASS ADJTHREAD
#-------------------------------------------------------------------------------
class AdjThread(QtCore.QThread):

    updateSignal = QtCore.pyqtSignal(object)
    plotSignal = QtCore.pyqtSignal(object)

# METHOD INIT
#-------------------------------------------------------------------------------
    def __init__(self, app, updateSemaphore, environment, simulationLength, plotIndices):
        QtCore.QThread.__init__(self, parent=app)
        self.environment = environment
        self.updateSemaphore = updateSemaphore
        self.simulationLength = simulationLength
        self.plotIndices = plotIndices

# METHOD RUN
#-------------------------------------------------------------------------------
    def run(self):
        self.environment.simulate(self.simulationLength, self, self.plotIndices)


#-------------------------------------------------------------------------------
# CLASS AGENT ELLIPSE
#-------------------------------------------------------------------------------
class AgentEllipse(QtWidgets.QGraphicsEllipseItem):
    """docstring for AgentEllipse."""

# METHOD INIT
#-------------------------------------------------------------------------------
    def __init__(self, agent, scene):
        QtWidgets.QGraphicsEllipseItem.__init__(self, 0, 0, agent.size, agent.size)
        self.setBrush(QtGui.QBrush(agent.color, style = agent.style))
        self.agent = agent
        self.oldXCoord = agent.xCoord
        self.oldYCoord = agent.yCoord
        self.exitAnimationComplete = False;
        self.setPos(agent.xCoord, agent.yCoord)


# METHOD HOVER EVENT ENTER
#-------------------------------------------------------------------------------
    def hoverEnterEvent(self, event):
        pass

# METHOD HOVER EVENT LEAVE
#-------------------------------------------------------------------------------
    def hoverLeaveEvent(self, event):
        pass

#-------------------------------------------------------------------------------
# CLASS ADJGRAPHICSVIEW
#-------------------------------------------------------------------------------
class AdjGraphicsView(QtWidgets.QGraphicsView):
    """docstring for GraphicsView."""

# METHOD init
#-------------------------------------------------------------------------------
    def __init__(self, screenGeometry, updateSemaphore):
        QtWidgets.QGraphicsView.__init__(self)
        # set Qt properties
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        # init scene
        self.windowHeight = screenGeometry.height() - 100
        self.windowWidth = screenGeometry.width() - 100
        centerWidth = self.windowWidth / -2
        centerHeight = self.windowHeight / -2

        self.scene = QtWidgets.QGraphicsScene(-500, -500, 1000, 1000, self)
        self.setScene(self.scene)

        # init other member variables
        self.graphicsItems = {}
        self.timeline = None
        self.animations = []
        self.updateSemaphore = updateSemaphore

        # show
        self.show()

# METHOD TIMESTEP ANIMATION CALLBACK
#-------------------------------------------------------------------------------
    def timestepAnimationCallback(self):
        self.updateSemaphore.release(1)

# METHOD UPDATE
#-------------------------------------------------------------------------------
    @QtCore.pyqtSlot(object)
    def update(self, agentSet):

        # begin update function
        self.animations.clear()
        del self.timeline
        self.timeline = QtCore.QTimeLine(200)
        self.timeline.setFrameRange(0, 200)
        self.timeline.finished.connect(self.timestepAnimationCallback)

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

                # animation = QtCore.QPropertyAnimation()
                # animation.setTimeLine(self.timeline)
                # animation.setItem(newEllipse)
                # animation.setScaleAt(0, 1, 1)
                # animation.setScaleAt(1, 100, 100)
                # self.animations.append(animation)

                self.scene.addItem(newEllipse)
            else:
                moveX = agent.xCoord - self.graphicsItems[agent].oldXCoord
                moveY = agent.yCoord - self.graphicsItems[agent].oldYCoord

                if moveX != 0 or moveY != 0:
                    # animation = QtCore.QPropertyAnimation()
                    # animation.setTimeLine(self.timeline)
                    # animation.setItem(self.graphicsItems[agent])
                    # animation.setPosAt(0, QtCore.QPointF(self.graphicsItems[agent].oldXCoord, \
                    #     self.graphicsItems[agent].oldYCoord))
                    # animation.setPosAt(1, QtCore.QPointF(agent.xCoord, agent.yCoord))
                    # self.animations.append(animation)

                    self.graphicsItems[agent].oldXCoord = agent.xCoord
                    self.graphicsItems[agent].oldYCoord = agent.yCoord

                    self.graphicsItems[agent].setPos(agent.xCoord, agent.yCoord)

        # remove graphics items whose agents are no longer in the agentset
        for item in self.graphicsItems.values():
            if item.agent not in agentSet:
                # destroy object with exit animation
                item.exitAnimationComplete = True
                # animation = QtCore.QPropertyAnimation()
                # animation.setTimeLine(self.timeline)
                # animation.setItem(item)
                # animation.setScaleAt(1, 1, 1)
                # animation.setScaleAt(0, 100, 100)
                # self.animations.append(animation)

        self.timeline.start()

# METHOD PLOT
#-------------------------------------------------------------------------------
    @QtCore.pyqtSlot(object)
    def plot(self, analysisIndex):
        analysisIndex.plot()
