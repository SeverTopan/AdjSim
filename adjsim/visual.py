
# standard
import sys
import time
import random

# third party
from PyQt5 import QtGui, QtCore, QtWidgets

# local
from . import simulation
from . import analysis

ANIMATION_DURATION = 200

class AdjThread(QtCore.QThread):

    update_signal = QtCore.pyqtSignal(object)

    def __init__(self, app, simulation, simulation_length=None):
        QtCore.QThread.__init__(self, parent=app)
        self.simulation = simulation
        self.update_semaphore = simulation._update_semaphore
        self.simulation_length = simulation_length

    def run(self):
        if self.simulation_length is not None:
            self.simulation._visual_simulate(self.simulation_length)
        else:
            self.simulation._visual_step()

class AgentEllipseAdapter(QtCore.QObject):
    """An adapter between QPropertyAnimation and QGraphicsEllipseItem

    This is in place because of PyQt's inablility to handle this functionality
    via multiple inheritance.
    """

    def __init__(self, target):
        super(AgentEllipseAdapter, self).__init__()
        self.target = target

    @QtCore.pyqtProperty(float)
    def x(self):
        return self.target.x()

    @x.setter
    def x(self, x):
        self.target.setX(x)

    @QtCore.pyqtProperty(float)
    def y(self):
        return self.target.y()

    @y.setter
    def y(self, y):
        self.target.setY(y)

    @QtCore.pyqtProperty(float)
    def size(self):
        return self.target.rect().width()

    @size.setter
    def size(self, size):
        newRect = self.target.rect()
        newRect.setWidth(size)
        newRect.setHeight(size)
        self.target.setRect(newRect)


class AgentEllipse(QtWidgets.QGraphicsEllipseItem):
    """docstring for AgentEllipse."""

    def __init__(self, agent, scene):
        QtWidgets.QGraphicsEllipseItem.__init__(self, 0, 0, 0, 0)
        self.setBrush(QtGui.QBrush(agent.color, style=agent.style))
        self.agent = agent
        self.old_x = agent.x
        self.old_y = agent.y
        self.exit_animation_complete = False
        self.setPos(agent.x, agent.y)
        self.adapter = AgentEllipseAdapter(self)


    def hoverEnterEvent(self, event):
        pass

    def hoverLeaveEvent(self, event):
        pass

class AdjGraphicsView(QtWidgets.QGraphicsView):
    """docstring for GraphicsView."""

    def __init__(self, screen_geometry, update_semaphore):
        QtWidgets.QGraphicsView.__init__(self)
        # set Qt properties
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        # init scene
        self.windowHeight = screen_geometry.height() - 100
        self.windowWidth = screen_geometry.width() - 100

        self.scene = QtWidgets.QGraphicsScene(-500, -500, 1000, 1000, self)
        self.setScene(self.scene)

        # init other member variables
        self.visual_items = {}
        self.timeline = None
        self.animations = None
        self.update_semaphore = update_semaphore

        # show
        self.show()

    def timestepAnimationCallback(self):
        self.update_semaphore.release(1)

    @QtCore.pyqtSlot(object)
    def update(self, agent_set):

        # begin update function
        del self.animations
        self.animations = QtCore.QParallelAnimationGroup()
        self.animations.finished.connect(self.timestepAnimationCallback)

        # delete items whose animations are complete
        for ellipse in self.visual_items.values():
            if ellipse.exit_animation_complete:
                self.scene.removeItem(ellipse)

        self.visual_items = {key: val for key, val in self.visual_items.items()
                             if not val.exit_animation_complete}

        # update agent ellipses
        for agent in agent_set:
            if not self.visual_items.get(agent.id):
                # create graphics item with entrance animation
                newEllipse = AgentEllipse(agent, self.scene)
                self.visual_items[agent.id] = newEllipse

                animation = QtCore.QPropertyAnimation(self.visual_items[agent.id].adapter, b'size')
                animation.setDuration(ANIMATION_DURATION)
                animation.setStartValue(0)
                animation.setEndValue(agent.size)
                self.animations.addAnimation(animation)

                self.scene.addItem(newEllipse)
            else:
                moveX = agent.x - self.visual_items[agent.id].old_x
                moveY = agent.y - self.visual_items[agent.id].old_y

                if moveX != 0 or moveY != 0:
                    animation = QtCore.QPropertyAnimation(self.visual_items[agent.id].adapter, b'x')
                    animation.setDuration(ANIMATION_DURATION)
                    animation.setStartValue(self.visual_items[agent.id].old_x)
                    animation.setEndValue(agent.x)
                    self.animations.addAnimation(animation)

                    animation = QtCore.QPropertyAnimation(self.visual_items[agent.id].adapter, b'y')
                    animation.setDuration(ANIMATION_DURATION)
                    animation.setStartValue(self.visual_items[agent.id].old_y)
                    animation.setEndValue(agent.y)
                    self.animations.addAnimation(animation)

                    self.visual_items[agent.id].old_x = agent.x
                    self.visual_items[agent.id].old_y = agent.y

        # remove graphics items whose agents are no longer in the agent_set
        agent_dict = {agent.id: agent for agent in agent_set}
        for key, val in self.visual_items.items():
            if not agent_dict.get(key, val):
                # destroy object with exit animation
                val.exit_animation_complete = True

                animation = QtCore.QPropertyAnimation(val.adapter, b'size')
                animation.setDuration(ANIMATION_DURATION)
                animation.setStartValue(val.agent.size)
                animation.setEndValue(0)
                self.animations.addAnimation(animation)

        self.animations.start()
