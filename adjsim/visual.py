"""Core AdjSim Module.

This module contains the core features of the ABM engine, specifically, the Simulation and Agent objects
and the facilities to allow them to interact with one another.

Designed and developed by Sever Topan.
"""

# Standard.
import sys
import time
import random

# Third party.
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np

# Local.
from . import core
from . import analysis

ANIMATION_DURATION = 200

class AdjThread(QtCore.QThread):
    """PyQt must run on the main thread, so we use this thread to run the simulation"""
    update_signal = QtCore.pyqtSignal(object)

    def __init__(self, app, simulation, simulation_length=None):
        QtCore.QThread.__init__(self, parent=app)
        self.simulation = simulation
        self.update_semaphore = simulation._update_semaphore
        self.simulation_length = simulation_length

    def run(self):
        """Run the simulation upon thread initialization."""
        self.simulation._super_step(self.simulation_length)

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
    """The Ellipse that represents the visual agents."""

    def __init__(self, agent, scene):
        QtWidgets.QGraphicsEllipseItem.__init__(self, 0, 0, 0, 0)

        # Members.
        self.agent = agent
        self.exit_animation_complete = False
        self.adapter = AgentEllipseAdapter(self)

        # Init visual.
        self.setBrush(QtGui.QBrush(agent.color, style=agent.style))
        self.setPos(agent.x, agent.y)

    def hoverEnterEvent(self, event):
        # TODO.
        pass

    def hoverLeaveEvent(self, event):
        # TODO.
        pass

class AdjGraphicsView(QtWidgets.QGraphicsView):
    """The Graphics View of the Visual Simulation."""

    def __init__(self, screen_geometry, update_semaphore):
        QtWidgets.QGraphicsView.__init__(self)

        # Set Qt properties.
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        # Init scene.
        self.windowHeight = screen_geometry.height() - 100
        self.windowWidth = screen_geometry.width() - 100

        self.scene = QtWidgets.QGraphicsScene(-500, -500, 1000, 1000, self)
        self.setScene(self.scene)

        # Init other member variables.
        self.visual_items = {}
        self.animations = None
        self.update_semaphore = update_semaphore

        # Show.
        self.show()

    def timestepAnimationCallback(self):
        self.update_semaphore.release(1)

    @QtCore.pyqtSlot(object)
    def update(self, agent_set):
        """The Visual update method, called after each timestep.

        Args:
            agent_set (list): The list of VisualAgent objects that will be rendered.
        """
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
                # Create graphics item with entrance animation.
                newEllipse = AgentEllipse(agent, self.scene)
                self.visual_items[agent.id] = newEllipse

                animation = QtCore.QPropertyAnimation(self.visual_items[agent.id].adapter, b'size')
                animation.setDuration(ANIMATION_DURATION)
                animation.setStartValue(0)
                animation.setEndValue(agent.size)
                self.animations.addAnimation(animation)

                self.scene.addItem(newEllipse)
            else:
                # Move animation.
                visual_item = self.visual_items[agent.id]
                if not np.array_equal(agent.pos, visual_item.agent.pos):
                    animation = QtCore.QPropertyAnimation(visual_item.adapter, b'x')
                    animation.setDuration(ANIMATION_DURATION)
                    animation.setStartValue(float(visual_item.agent.x))
                    animation.setEndValue(float(agent.x))
                    self.animations.addAnimation(animation)

                    animation = QtCore.QPropertyAnimation(visual_item.adapter, b'y')
                    animation.setDuration(ANIMATION_DURATION)
                    animation.setStartValue(float(visual_item.agent.y))
                    animation.setEndValue(float(agent.y))
                    self.animations.addAnimation(animation)

                    # Store.
                    visual_item.agent.pos = agent.pos

            # Update color.
            visual_item = self.visual_items[agent.id]
            if agent.color != visual_item.agent.color or \
                    agent.style != visual_item.agent.style:
                # Paint.
                visual_item.setBrush(QtGui.QBrush(agent.color, style=agent.style))

                # Store.
                visual_item.agent.color = agent.color
                visual_item.agent.style = agent.style


        # remove graphics items whose agents are no longer in the agent_set
        agent_dict = {agent.id: agent for agent in agent_set}
        for key, val in self.visual_items.items():
            if not agent_dict.get(key):
                # destroy object with exit animation
                val.exit_animation_complete = True

                animation = QtCore.QPropertyAnimation(val.adapter, b'size')
                animation.setDuration(ANIMATION_DURATION)
                animation.setStartValue(val.agent.size)
                animation.setEndValue(0)
                self.animations.addAnimation(animation)

        self.animations.start()
