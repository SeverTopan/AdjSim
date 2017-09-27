# standard
import random
import time
import sys
import uuid
import copy

# third party
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

# local
from . import utility
from . import analysis
from . import visual
from . import decision
from . import color
from . import index
from . import callback

class _ActionSuite(utility.InheritableDict):

    def __setitem__(self, key, value):
        if not callable(value):
            raise utility.InvalidActionException

        self._data[key] = value

class Agent(object):
    """docstring for Agent."""

    def __init__(self):
        self.actions = _ActionSuite()
        self.decision = decision.NoCastDecision()
        self.order = 0
        self.id = uuid.uuid4()
        self.step_complete = False
        
        self._exists = True
        self._movement_callback = None

class SpatialAgent(Agent):
    """
    """

    DEFAULT_POS = np.array([0, 0])

    def __init__(self, pos=DEFAULT_POS):
        super().__init__()
        self._pos = pos

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        # assert pos type
        if not type(value) == np.ndarray or value.shape != (2,):
            raise TypeError
        
        # Make immutable so that we have control over the agent movement callback.
        value.flags.writeable = False

        self._pos = value

        # Trigger callback.
        # This will always be non-None if the agent has been added to a simulation.
        if self._movement_callback is not None:
            self._movement_callback(self)

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos = np.array([value, self.y])

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos = np.array([self.x, value])


class VisualAgent(SpatialAgent):
    """docstring for Agent."""

    DEFAULT_SIZE = 10
    DEFAULT_COLOR = color.BLUE_DARK
    DEFAULT_STYLE = QtCore.Qt.SolidPattern

    def __init__(self, pos=SpatialAgent.DEFAULT_POS, size=DEFAULT_SIZE, color=DEFAULT_COLOR,
                 style=DEFAULT_STYLE):
        super().__init__(pos)
        self.size = size
        self.color = color
        self.style = style

class _AgentSuite(utility.InheritableSet):

    def __init__(self, callback_suite):
        super().__init__()

        # Store references for callbacks
        self.callback_suite = callback_suite

    def add(self, agent):
        if not issubclass(type(agent), Agent):
            raise utility.InvalidAgentException

        # Add agent.
        self._data.add(agent)

        # Register movement callback.
        agent._movement_callback = self.callback_suite.agent_moved

        # Trigger addition callback.
        self.callback_suite.agent_added(agent)

    def discard(self, value):
        # 'Euthanize' and remove agent.
        value._exists = False
        value.step_complete = True
        return_val = self._data.discard(value)

        # Trigger callbacks.
        self.callback_suite.agent_removed(value)

        return return_val

    def visual_snapshot(self):
        return_set = set()

        for agent in self._data:
            if issubclass(type(agent), VisualAgent):
                visual_copy = VisualAgent(pos=copy.copy(agent.pos), size=copy.copy(agent.size), 
                                          color=copy.copy(agent.color), style=copy.copy(agent.style))
                visual_copy.id = copy.copy(agent.id)
                return_set.add(visual_copy)

        return return_set


class _TrackerSuite(utility.InheritableDict):

    def __setitem__(self, key, value):
        try:
            assert issubclass(type(value), analysis.Tracker)
        except:
            raise utility.InvalidTrackerException

        self._data[key] = value

class _CallbackSuite(object):
    def __init__(self):
        self.agent_added = callback.AgentChangedCallback()
        self.agent_removed = callback.AgentChangedCallback()
        self.agent_moved = callback.AgentChangedCallback()


class _IndexSuite(object):
    def __init__(self, simulation):
        self._grid = None
        self._simulation = simulation

    @property
    def grid(self):
        return self._grid()

    def initialize_grid(self):
        self._grid = index.GridIndex(self._simulation)


class Simulation(object):
    """docstring for Environment."""

    def __init__(self):
        self.callbacks = _CallbackSuite()
        self.agents = _AgentSuite(self.callbacks)
        self.trackers = _TrackerSuite()
        self.end_condition = None
        self.time = 0

        self._prev_print_str_len = 0

    @staticmethod
    def _print_banner():
        welcomeMessage = "- AdjSim Reinforcement-Learning ABM Engine -"

        print("-".rjust(len(welcomeMessage), "-"))
        print(welcomeMessage)
        print("-".rjust(len(welcomeMessage), "-"))


    def step(self):
        # Perform setup in needed.
        if self.time == 0:
            self._track()

        # Iterate through agents in sorted order
        for agent in sorted(self.agents, key=lambda a: a.order):
            # Check if agent has been removed in previous iteration
            if not agent._exists:
                continue

            # Delegate action casting to decision module.
            try:
                agent.decision(self, agent)
            except TypeError:
                raise utility.InvalidDecisionException

            agent.step_complete = False

        self.time += 1

        self._track()


    def simulate(self, num_timesteps):

        for i in range(num_timesteps):
            self._print_simulation_status(i + 1, num_timesteps)
    
            self.step()

            # Check end condition.
            if self.end_condition is not None:
                try:
                    if self.end_condition(self):
                        break

                except TypeError:
                    raise utility.InvalidEndConditionException


    def _track(self):
        try:
            for tracker in self.trackers.values():
                tracker(self)
        except:
            raise utility.InvalidTrackerException


    def _print_simulation_status(self, timestep, num_timesteps):
        # Flush previous message.
        sys.stdout.write("\r" + " " * self._prev_print_str_len)
        sys.stdout.flush()

        # Print new timestep string.
        print_str = "\rSimulating timestep " + str(timestep) + "/" + str(num_timesteps) + " - population: " \
                + str(len(self.agents))
        sys.stdout.write(print_str)
        sys.stdout.flush()

        self._prev_print_str_len = len(print_str)

        
class VisualSimulation(Simulation):

    def __init__(self):
        super().__init__()

        self._multistep_simuation_in_progress = False
        self._setup_required = True
        self._wait_on_visual_init = 1


    def _run_visual(self, num_timestep=None):
        # Perform threading initialization for graphics.
        self._update_semaphore = QtCore.QSemaphore(0)
        self._q_app = QtWidgets.QApplication([]) 
        self._view = visual.AdjGraphicsView(self._q_app.desktop().screenGeometry(), self._update_semaphore)
        self._visual_thread = visual.AdjThread(self._q_app, self, num_timestep)

        self._visual_thread.finished.connect(self._q_app.exit)
        self._visual_thread.update_signal.connect(self._view.update)

        # Begin simulation.
        self._visual_thread.start()
        self._q_app.exec_()


        # Cleanup variables.
        self._visual_thread.quit()
        del self._visual_thread
        del self._view
        del self._q_app
        del self._update_semaphore


    def _visual_step(self):
        # Paint initial frame.
        if self._setup_required:
            self._setup_required = False
            self._visual_thread.update_signal.emit(self.agents.visual_snapshot())
            time.sleep(self._wait_on_visual_init)

        super().step()

        # Wait for animaiton.
        self._visual_thread.update_semaphore.acquire(1)
        self._visual_thread.update_signal.emit(self.agents.visual_snapshot())


    def _visual_simulate(self, num_timesteps):
        super().simulate(num_timesteps)


    def step(self):
        if self._multistep_simuation_in_progress:
            self._visual_step()
        else:
            self._setup_required = True
            self._run_visual()
        

    def simulate(self, num_timesteps):
        self._multistep_simuation_in_progress = True
        self._setup_required = True

        self._run_visual(num_timesteps)

        self._multistep_simuation_in_progress = False

            