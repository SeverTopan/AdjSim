"""Core adjsim module.

This module contains the core features of the ABM engine, specifically, the Simulation and Agent objects
and the facilities to allow them to interact with one another.

Designed and developed by Sever Topan.
"""

# Standard.
import random
import time
import sys
import uuid
import copy

# Third party.
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

# Local.
from . import utility
from . import analysis
from . import visual
from . import decision
from . import color
from . import index
from . import callback

class _ActionSuite(utility.InheritableDict):
    """Container for Actions. May only store callables.

    This object behaves through the same interface as a python 
    dictionary.
    """

    def __setitem__(self, key, value):
        """Adds an item to the action suite."""
        if not callable(value):
            raise utility.ActionException

        self._data[key] = value

class Agent(object):
    """The base Agent class. 
    
    All agents added to a simulation must be derived from this.

    Attributes:
        actions (_ActionSuite): The _ActionSuite container that holds all actions.
        decision (decision.Decision): The decision object that the agent will use to determine action invocation.
        order (int): The order in which this agent will take its step relative to others. Equal orders result in
            no step order guarantee.
        step_complete (bool): whether or not the agent has completed its step.
    """

    def __init__(self):
        self.actions = _ActionSuite()
        self.decision = decision.NoCastDecision()
        self.order = 0
        self.step_complete = False
        
        self._exists = True
        self._id = uuid.uuid4()        

    @property
    def id(self):
        """ uuid: A unique identifier for the agent. Read-only."""
        return self._id

class SpatialAgent(Agent):
    """The Spatial Agent class. 
    
    Builds upon Agent to incorporate 2d spatial coordinates representing the agent's position.
    Any agent that desires to have the movement callback invoked when position is changed should
    inherit from this class.
    """

    DEFAULT_POS = np.array([0, 0])

    def __init__(self, pos=DEFAULT_POS):
        super().__init__()
        self._pos = None
        self._movement_callback = None

        # Go through setter so that we do proper type checks.
        self.pos = pos
        

    @property
    def pos(self):
        """np.ndarray: Obtains agent position. The returned array is NOT writeable."""
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
        """int: Obtains agent's x-coordinate."""
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos = np.array([value, self.y])

    @property
    def y(self):
        """int: Obtains agent's y-coordinate."""
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos = np.array([self.x, value])


class VisualAgent(SpatialAgent):
    """The Visual Agent class. 
    
    Builds upon SpatialAgent to allow for agents to be visualized when simulated with a VisualSimulation.
    Visual agents appear as circles with visual properties delineated by this class's attributes.

    Attributes:
        size (int): The size of the visualized agent.
        color (QtGui.QColor): The color of the visualized agent.
        style (QtCore.Qt.Pattern): The pattern of the visualized agent.
    """

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
    """Container for agents. May only store objects derived from Agent.

    This object behaves through the same interface as a python set. 
    One additional function is provided to obtain a set copy for use in visualization.

    Attributes:
        callback_suite (_CallbackSuite): Reference to the simulation callback suite.
    """

    def __init__(self, callback_suite):
        super().__init__()

        # Store references for callbacks
        self.callback_suite = callback_suite

    def add(self, agent):
        """Adds an item to the agent suite."""
        if not issubclass(type(agent), Agent):
            raise utility.InvalidAgentException

        # Add agent.
        self._data.add(agent)

        # Register movement callback.
        if issubclass(type(agent), SpatialAgent):
            agent._movement_callback = self.callback_suite.agent_moved

        # Trigger addition callback.
        self.callback_suite.agent_added(agent)

    def discard(self, value):
        """Discards an item to the agent suite."""
        # 'Euthanize' and remove agent.
        value._exists = False
        value.step_complete = True
        return_val = self._data.discard(value)

        # Trigger callbacks.
        self.callback_suite.agent_removed(value)

        return return_val

    def visual_snapshot(self):
        """Obtains a copy of the agent suite for visualization.
        
        Returns:
            A set of VisualAgent objects.
        """
        return_set = set()

        for agent in self._data:
            if issubclass(type(agent), VisualAgent):
                visual_copy = VisualAgent(pos=copy.copy(agent.pos), size=copy.copy(agent.size), 
                                          color=copy.copy(agent.color), style=copy.copy(agent.style))
                visual_copy._id = copy.copy(agent.id)
                return_set.add(visual_copy)

        return return_set


class _TrackerSuite(utility.InheritableDict):
    """Container for trackers. May only store objects derived from Tracker.

    This object behaves through the same interface as a python dictionary. 
    """

    def __setitem__(self, key, value):
        """Adds an item to the tracker suite."""
        try:
            assert issubclass(type(value), analysis.Tracker)
        except:
            raise utility.TrackerException

        self._data[key] = value

class _CallbackSuite(object):
    """Container for callbacks.

    Attributes:
        agent_added (callback.AgentChangedCallback): Fires when an Agent is added to the agent set.
        agent_removed (callback.AgentChangedCallback): Fires when an Agent is removed from the agent set.
        agent_moved (callback.AgentChangedCallback): Fires when a SpatialAgent's pos attribute is set.
        simulation_step_started (callback.SimulationMilestoneCallback): Fires when a Simulation step is started.
        simulation_step_complete (callback.SimulationMilestoneCallback): Fires when a Simulation step is ended.
        simulation_started (callback.SimulationMilestoneCallback): Fires when the Simulation starts.
        simulation_complete (callback.SimulationMilestoneCallback): Fires when the Simulation ends.
        
    """

    def __init__(self):
        # Agent callbacks.
        self.agent_added = callback.AgentChangedCallback()
        self.agent_removed = callback.AgentChangedCallback()
        self.agent_moved = callback.AgentChangedCallback()
        
        self.simulation_step_started = callback.SimulationMilestoneCallback()
        self.simulation_step_complete = callback.SimulationMilestoneCallback()
        self.simulation_started = callback.SimulationMilestoneCallback()
        self.simulation_complete = callback.SimulationMilestoneCallback()


class _IndexSuite(object):
    """Container for indidces.
    """

    def __init__(self, simulation):
        self._grid = index.GridIndex(simulation)

    @property
    def grid(self):
        """Obtain the grid index."""
        return self._grid



class Simulation(object):
    """The base Simulation object.

    This is the core object that is used to run adjsim simulations.

    Attributes:
        callbacks (_CallbackSuite): The Simulation's callbacks.
        agents (_AgentSuite): The Simulation's agents.
        trackers (_TrackerSuite): The Simulation's trackers.
        indices (_IndexSuite): The Simulation's indices.
        end_condition (callable): The Simulation's end condition.
        time (int): The current Simulation time. Reflects step count.
    """

    def __init__(self):
        self.callbacks = _CallbackSuite()
        self.agents = _AgentSuite(self.callbacks)
        self.trackers = _TrackerSuite()
        self.indices = _IndexSuite(self)
        self.end_condition = None
        self.time = 0

        self._prev_print_str_len = 0
        self._running = False

    def start(self):
        """Starts a simulation instance.

        Note:
            This must be called before a call to the step function. This function triggers the
            simulation_started callback.
        """
        if self._running == True:
            raise Exception("Simulation already started.")

        self._running = True

        # Call milestone callback.
        self.callbacks.simulation_started(self)


    def end(self):
        """Ends a simulation instance.

        Note:
            This function triggers the simulation_ended callback.
        """
        if self._running == False:
            raise Exception("Simulation already ended.")

        self._running = False

        # Print a new line for prettier formatting.
        print()

        # Call milestone callback.
        self.callbacks.simulation_complete(self)


    def _step_single(self):
        """Performs a single simulation step. 
        
        This is where one iteration of the ABM loop occurs.
        """
        # Perform setup in needed.
        if self.time == 0:
            self._track()

        # Call milestone callback.
        self.callbacks.simulation_step_started(self)

        # Iterate through agents in sorted order
        for agent in sorted(self.agents, key=lambda a: a.order):
            # Check if agent has been removed in previous iteration
            if not agent._exists:
                continue

            # Delegate action casting to decision module.
            try:
                agent.decision(self, agent)
            except:
                raise utility.DecisionException

            agent.step_complete = False

        self.time += 1

        self._track()

        # Call milestone callback.
        self.callbacks.simulation_step_complete(self)


    def step(self, num_timesteps=1):
        """Performs a given number of simulation steps. 
        
        Note:
            This is where ABM loop occurs. This function must be called after the simulation has been started.

        Args:
            num_timesteps (int): the number of timesteps to simulate.
        """
        # Check running status.
        if not self._running:
            raise utility.SimulatonWorkflowException()

        # Simulate.
        for i in range(num_timesteps):
            self._print_simulation_status(i + 1, num_timesteps)
    
            self._step_single()

            # Check end condition.
            if self.end_condition is not None:
                try:
                    if self.end_condition(self):
                        break

                except:
                    raise utility.EndConditionException

    def simulate(self, num_timesteps):
        """Performs a given number of simulation steps while handling simulation start/end.
        
        Note:
            This convinience method simply calls start, step(num_timesteps), and end.

        Args:
            num_timesteps (int): the number of timesteps to simulate.
        """
        self.start()
        self.step(num_timesteps)
        self.end()

    def _track(self):
        """Calls the Simulation's trackers."""
        try:
            for tracker in self.trackers.values():
                tracker(self)
        except:
            raise utility.TrackerException


    def _print_simulation_status(self, timestep, num_timesteps):
        """Prints the simulation status at a given timestep.
        
        Args:
            timestep (int): The current timestep.
            num_timesteps (int): The total number of timesteps.
        """
        # Flush previous message.
        sys.stdout.write("\r" + " " * self._prev_print_str_len)
        sys.stdout.flush()

        # Print new timestep string.
        print_str = "\rSimulating timestep {}/{} - population: {}".format(timestep, num_timesteps, len(self.agents))
        sys.stdout.write(print_str)
        sys.stdout.flush()

        self._prev_print_str_len = len(print_str)

        
class VisualSimulation(Simulation):
    """The Visual Simulation object.

    This derivation of the Simulation object uses PyQt5 to render a visual representation
    of an active simulation.
    """

    def __init__(self):
        super().__init__()

        self._setup_required = True
        self._wait_on_visual_init = 1

    def _super_step(self, num_timesteps):
        """Calls the step method on Simulation base.
        
        Args:
            num_timesteps (int): The number of timesteps to simulate.
        """
        super().step(num_timesteps)

    def _step_single(self):
        """Visual implementation of single step."""
        # Paint initial frame.
        if self._setup_required:
            self._setup_required = False
            self._visual_thread.update_signal.emit(self.agents.visual_snapshot())
            time.sleep(self._wait_on_visual_init)

        super()._step_single()

        # Wait for animaiton.
        self._visual_thread.update_semaphore.acquire(1)
        self._visual_thread.update_signal.emit(self.agents.visual_snapshot())

    def step(self, num_timesteps=1):
        """Perform a given number of visual simulation steps.
        
        Args:
            num_timesteps (int): The number of timesteps to simulate.
        """
        # Check running status.
        if not self._running:
            raise utility.SimulatonWorkflowException()

        # Perform threading initialization for graphics.
        self._setup_required = True
        self._update_semaphore = QtCore.QSemaphore(0)
        self._q_app = QtWidgets.QApplication([]) 
        self._view = visual.AdjGraphicsView(self._q_app.desktop().screenGeometry(), self._update_semaphore)
        self._visual_thread = visual.AdjThread(self._q_app, self, num_timesteps)

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
