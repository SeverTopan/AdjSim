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
# CONSTANTS
#-------------------------------------------------------------------------------
ANIMATION_DURATION = 200

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
# CLASS AGENT ELLIPSE ADAPTER
#-------------------------------------------------------------------------------
class AgentEllipseAdapter(QtCore.QObject):
    """An adapter between QPropertyAnimation and QGraphicsEllipseItem

    This is in place because of PyQt's inablility to handle this functionality
    via multiple inheritance.
    """

# METHOD INIT
#-------------------------------------------------------------------------------
    def __init__(self, target):
        super(AgentEllipseAdapter, self).__init__()
        self.target = target

# METHOD GET X
#-------------------------------------------------------------------------------
    @QtCore.pyqtProperty(float)
    def x(self):
        return self.target.x()

# METHOD SET X
#-------------------------------------------------------------------------------
    @x.setter
    def x(self, x):
        self.target.setX(x)

# METHOD GET Y
#-------------------------------------------------------------------------------
    @QtCore.pyqtProperty(float)
    def y(self):
        return self.target.y()

# METHOD SET Y
#-------------------------------------------------------------------------------
    @y.setter
    def y(self, y):
        self.target.setY(y)

# METHOD GET SIZE
#-------------------------------------------------------------------------------
    @QtCore.pyqtProperty(float)
    def size(self):
        return self.target.rect().width()

# METHOD SET SIZE
#-------------------------------------------------------------------------------
    @size.setter
    def size(self, size):
        newRect = self.target.rect()
        newRect.setWidth(size)
        newRect.setHeight(size)
        self.target.setRect(newRect)


#-------------------------------------------------------------------------------
# CLASS AGENT ELLIPSE
#-------------------------------------------------------------------------------
class AgentEllipse(QtWidgets.QGraphicsEllipseItem):
    """docstring for AgentEllipse."""

# METHOD INIT
#-------------------------------------------------------------------------------
    def __init__(self, agent, scene):
        QtWidgets.QGraphicsEllipseItem.__init__(self, 0, 0, 0, 0)
        self.setBrush(QtGui.QBrush(agent.color, style = agent.style))
        self.agent = agent
        self.oldXCoord = agent.xCoord
        self.oldYCoord = agent.yCoord
        self.exitAnimationComplete = False;
        self.setPos(agent.xCoord, agent.yCoord)
        self.adapter = AgentEllipseAdapter(self)


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
        self.animations = None
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
        del self.animations
        self.animations = QtCore.QParallelAnimationGroup()
        self.animations.finished.connect(self.timestepAnimationCallback)

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

                animation = QtCore.QPropertyAnimation(self.graphicsItems[agent].adapter, b'size')
                animation.setDuration(ANIMATION_DURATION);
                animation.setStartValue(0)
                animation.setEndValue(agent.size)
                self.animations.addAnimation(animation)

                self.scene.addItem(newEllipse)
            else:
                moveX = agent.xCoord - self.graphicsItems[agent].oldXCoord
                moveY = agent.yCoord - self.graphicsItems[agent].oldYCoord

                if moveX != 0 or moveY != 0:
                    animation = QtCore.QPropertyAnimation(self.graphicsItems[agent].adapter, b'x')
                    animation.setDuration(ANIMATION_DURATION);
                    animation.setStartValue(self.graphicsItems[agent].oldXCoord)
                    animation.setEndValue(agent.xCoord)
                    self.animations.addAnimation(animation)

                    animation = QtCore.QPropertyAnimation(self.graphicsItems[agent].adapter, b'y')
                    animation.setDuration(ANIMATION_DURATION);
                    animation.setStartValue(self.graphicsItems[agent].oldYCoord)
                    animation.setEndValue(agent.yCoord)
                    self.animations.addAnimation(animation)

                    self.graphicsItems[agent].oldXCoord = agent.xCoord
                    self.graphicsItems[agent].oldYCoord = agent.yCoord

        # remove graphics items whose agents are no longer in the agentset
        for item in self.graphicsItems.values():
            if item.agent not in agentSet:
                # destroy object with exit animation
                item.exitAnimationComplete = True

                animation = QtCore.QPropertyAnimation(self.graphicsItems[item.agent].adapter, b'size')
                animation.setDuration(ANIMATION_DURATION);
                animation.setStartValue(item.agent.size)
                animation.setEndValue(0)
                self.animations.addAnimation(animation)

        self.animations.start()

# METHOD PLOT
#-------------------------------------------------------------------------------
    @QtCore.pyqtSlot(object)
    def plot(self, analysisIndex):
        analysisIndex.plot()
