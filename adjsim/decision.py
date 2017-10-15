"""Decision module.

This module contains the different decision functors used by agents to call actions.
Also contains helper classes used by these.

Designed and developed by Sever Topan.
"""

# Standard.
import os
import sys
import re
import pickle
import random
import re

# Local.
from . import utility

class DecisionMutableFloat(object):
    """Contains a bounded float that the decision module will modify.

    A decision mutable float represents a value that a particular decision module will try to optimize for.
    This float must be given viable bounds between which the decision module will try to find an optimal 
    value to fulfill its loss function.
    """
    def __init__(self, min_val, max_val):
        self._value = float(max_val - min_val)
        self._min_val = min_val
        self._max_val = max_val

    @property
    def value(self):
        """float: Obtain the value."""
        return self._value

    @property
    def min_val(self):
        """float: Obtain the minimum bound."""
        return self._min_val

    @property
    def max_val(self):
        """float: Obtain the maximum bound."""
        return self._max_val

    def _set_value(self, value):
        """Private setter for use by decision modules."""
        if value < self._min_val or value > self._max_val:
            raise ValueError

        self._value = value

class _DecisionMutablePremise(object):
    """Container for a decision mutable in an action premise iteration.

    Attributes:
        name (string): The decision mutable attribute name.
        value (object): The value of the decision mutable.
    """

    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value

    def set(self, target):
        getattr(target, self.name)._set_value(self.value)

    def __repr__(self):
        """Debug printing."""
        return "(" + str(self.name) + " - " + str(self.value) + ")"


class _ActionPremiseIteration(object):
    """Container for an action premse iteration.

    Contains one iteration of an _ActionPremise.

    Attributes:
        action_name (string): The action name.
        decision_mutables (list): The list of _DecisionMutablePremise objects.
    """

    def __init__(self, action_name=None, decision_mutables=None):
        self.action_name = action_name
        self.decision_mutables = [] if decision_mutables is None else decision_mutables

    def set_mutables(self, target):
        """Sets the decision mutable attributes in the iteration.
        
        Args:
            source (Agent): The target agent to have its decision-mutables set.
        """
        try:
            for decision_mutable in self.decision_mutables:
                decision_mutable.set(target)
        except:
            raise utility.MissingAttributeException

    def call_action(self, simulation, source):
        """Calls the action in the iteration.
        
        Args:
            simulation (Simulation): The Simulation.
            source (Agent): The source agent.
        """
        action = source.actions.get(self.action_name)
        if action is None:
            raise utility.MissingAttributeException
        
        action(simulation, source)

    def __repr__(self):
        """Debug printing."""
        return str(self.action_name) + " - " + str(self.decision_mutables)

class _ActionPremise(object):
    """Container for an action premse.

    An action premise is a representation of a series of actions for an agent to call
    alongside a series of values to attribute to an agent's decision mutable attributes.

    It is basically a snapshot of the computation that an agent can do during a simulation step.

    Attributes:
        iterations (list): The list of _ActionPremiseIteration objects.
    """
    def __init__(self, iterations=None):
        self.iterations = [] if iterations is None else iterations
        

    def call(self, simulation, source):
        """Calls the action premise.
        
        Args:
            simulation (Simulation): The Simulation.
            source (Agent): The source agent.
        """
        # Call all iterations.
        for iteration in self.iterations:
            # Check if complete.
            if source.step_complete:
                return

            # Setup and cast.
            iteration.set_mutables(source)
            iteration.call_action(simulation, source)

    def __repr__(self):
        """Debug printing."""
        return str(self.iterations)

class Decision(object):
    """The base decision class.

    A decision is a functor that performs selective and structured agent computation during a
    simulation step.
    """

    def __call__(self, simulation, source):
        """Perform computation."""
        raise NotImplementedError

class NoCastDecision(object):
    """A decision to not do any computation during a simulation step.
    """
    def __call__(self, simulation, source):
        """Perform no computation."""
        return

class RandomSingleCastDecision(Decision):
    """A decision to cast a single randomly-chosen action during a simulation step.
    """

    def __call__(self, simulation, source):
        """Call a single randomly-selected action."""
        # If no actions to choose from, skip.
        if len(source.actions) == 0:
            return

        # Set decision mutable values to random values.
        decision_mutable_names = [d for d in dir(source) if type(getattr(source, d)) == DecisionMutableFloat]
        for decision_mutable_name in decision_mutable_names:
            decision_mutable = getattr(source, decision_mutable_name)
            value = random.uniform(decision_mutable.min_val, decision_mutable.max_val)
            decision_mutable._set_value(value)

        # Randomly execute an action.
        try:
            action = random.choice(list(source.actions.values()))
            action(simulation, source)
        except:
            raise utility.ActionException

class RandomRepeatedCastDecision(Decision):
    """A decision to cast multiple randomly-chosen action during a simulation step.

    Actions are repeatedly cast until the agent's step_complete attribute is set to True.
    """

    def __call__(self, simulation, source):
        # If no actions to choose from, skip.
        if len(source.actions) == 0:
            return

        # Randomly execute an action while the agent has not completed their timestep.
        while not source.step_complete:
            # Set decision mutable values to random values.
            decision_mutable_names = [d for d in dir(source) if type(getattr(source, d)) == DecisionMutableFloat]
            for decision_mutable_name in decision_mutable_names:
                decision_mutable = getattr(source, decision_mutable_name)
                value = random.uniform(decision_mutable.min_val, decision_mutable.max_val)
                decision_mutable._set_value(value)

            try:
                action = random.choice(list(source.actions.values()))
                action(simulation, source)
            except:
                raise utility.ActionException

class FunctionalDecision(Decision):
    """An abastract decision class that uses adjsim's functional step implementation.

    Essentially, the agent acts as a function. The inputs to this function are retrieved from
    the perception callable. This is referred to as an observation. The observation is then used in
    the rest of the decision process to decide which action to call, and what to set decision mutable 
    values to.

    The loss callable is used to determine how well an agent is performing. The decision module can employ
    reinforcement learning through optimizing the loss function via intelligently selected action premises.

    Args:
        perception (callable): The perception callable. Can return any value.
        loss (callable): The loss callable. Must return a float-convertible object.
    """

    def __init__(self, perception, loss):
        self.perception = perception
        self.loss = loss

    def __call__(self, simulation, source):
        """Perform computation."""
        raise NotImplementedError

        
class _QLearningHistoryItem(object):
    """Container class for Q-Learning history items."""
    def __init__(self, observation, action_premise, loss):
        self.observation = observation
        self.action_premise = action_premise
        self.loss = loss

class _QTableEntry(object):
    """Container class for Q-Table entries."""
    def __init__(self, action_premise, loss):
        self.action_premise = action_premise
        self.loss = loss

    def __repr__(self):
        return self.loss + " : " + self.action_premise.__repr__()

class QLearningDecision(FunctionalDecision):
    """A decision module based on Q-Learning.

    This module employs Q-Learning (https://en.wikipedia.org/wiki/Q-learning), a reinforcement
    learning technique, to incrementally enhance its performance as measured by the provided loss
    function. Over many simulations, the performance of the agent will be increased.

    Args:
        perception (callable): The perception callable. Can return any value.
        loss (callable): The loss callable. Must return a float-convertible object.
        callbacks (_CallbackSuite): The simulation's callback suite. Used by the decision module
            to register neccessary callbacks.
        input_file_name (string): The name of the .pkl file from which to read a previous Q-Table.
            The previous Q-Table will be used as a starting point in the current simulation.
        output_file_name (string): The name of the .pkl file where the new Q-Table will be saved.
        discount_factor (float): The dscount factor (gamma) used in the temporal-differnce calculation
            of agent loss. Defaults to 0.95.
        nonconformity_probability (float): When an agent finds an existing entry in its Q-Table, it will 
            still choose to perform a random action with a probability equivalent to 
            nonconformity_probability. Defaults to 0.3.
    """

    DEFAULT_IO_FILE_NAME = re.sub("\.py", ".qlearning.pkl", sys.argv[0])
    PRINT_DEBUG = False
    DEFAULT_DISCOUNT_FACTOR = 0.95
    DEFAULT_NONCONFORMITY_FACTOR = 0.3

    history_bank = {}

    def __init__(self, perception, loss, callbacks,
                 input_file_name=DEFAULT_IO_FILE_NAME, output_file_name=DEFAULT_IO_FILE_NAME,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR, nonconformity_probability=DEFAULT_NONCONFORMITY_FACTOR):
        super().__init__(perception, loss)

        # Initialize members.
        self.q_table = {}
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.discount_factor = discount_factor
        self.nonconformity_probability = nonconformity_probability

        # Load q_table
        self._load_q_table_from_disk()

        # Register callbacks.
        callbacks.simulation_complete.register(self._on_simulation_complete)


    def _load_q_table_from_disk(self):
        """Loads the Q-Table from the file described by input_file_name"""
        # Print ui messages.
        if not self.input_file_name is None and os.path.isfile(self.input_file_name):
            sys.stdout.write("Q Learning training data found, loading from " + self.input_file_name + "...")
            sys.stdout.flush()
        else:
            print("Q Learning training data not found.")
            return

        # Load data.
        self.q_table = pickle.load(open(self.input_file_name, "rb"))

        # Ui messages.
        if QLearningDecision.PRINT_DEBUG:
            self.printBestMoveDict()
        sys.stdout.write("done\n")
        sys.stdout.flush()

    def printBestMoveDict(self):
        """Debug printing of the Q-Table"""
        for observation, item in self.q_table.items():
            print("   ", observation, " > ", item.action_premise)

    def __call__(self, simulation, source):
        """The functor call that executes Q-learning.

        Agents randomly choose actions if they have never encountered a particular
        observation before. Otherwise, They conditionally execute the previously encountered
        action premise (note nonconformity_probability).

        Information regarding randomly chosen abilities is stored in the history bank until
        simulation completion.

        Args:
            simulation (Simulation): The Simulation.
            source (Agent): The source Agent.
        """
        # Observe environment.
        observation = None
        try:
            observation = self.perception(simulation, source)
        except:
            raise utility.PerceptionException

        # Check for a known action premise.
        q_table_entry = self.q_table.get(observation)
        action_premise = q_table_entry.action_premise if not q_table_entry is None else None

        # Cast action.
        # The random action will still be called even if a q_table entry is found.
        # This happens with a probability represented by the nonconformity_probability.
        if action_premise is None or random.random() < self.nonconformity_probability:
            # Prepare action premise.
            action_premise = _ActionPremise()

            # This is essentially a RandomRepeatedCast.
            while not source.step_complete:
                action_premise_iteration = _ActionPremiseIteration()

                # Set decision mutable values to random values, save to action premise.
                decision_mutable_names = [d for d in dir(source) if type(getattr(source, d)) == DecisionMutableFloat]
                for decision_mutable_name in decision_mutable_names:
                    decision_mutable = getattr(source, decision_mutable_name)
                    value = random.uniform(decision_mutable.min_val, decision_mutable.max_val)

                    decision_mutable._set_value(value)
                    action_premise_iteration.decision_mutables.append(_DecisionMutablePremise(decision_mutable_name, value))

                # Cast fallback decision, save to action premise.
                try:
                    identifier, action = random.choice(list(source.actions.items()))
                    action(simulation, source)
                    action_premise_iteration.action_name = identifier
                except:
                    raise utility.ActionException

                # Save action premise.
                action_premise.iterations.append(action_premise_iteration)

        else:
            # Call the action premise.
            action_premise.call(simulation, source)

        # Obtain current loss.
        current_loss = None
        try:
            current_loss = self.loss(simulation, source)
        except:
            raise utility.LossException

        # Bank history.
        history_item = _QLearningHistoryItem(observation, action_premise, current_loss)
        agent_history = QLearningDecision.history_bank.get(source.id)
        if agent_history is None:
            QLearningDecision.history_bank[source.id] = [history_item]
        else:
            QLearningDecision.history_bank[source.id].append(history_item)

    def _update_q_table_from_history_bank(self):
        """Update Q-Table from the history bank.
        
        Apply temporal difference to the losses stored in the history bank, and store
        action premises that result in losses that are better than previously recorded 
        entries in the Q-Table.
        """
        # Ui.
        sys.stdout.write("Processing Q-Learning data...")
        sys.stdout.flush()

        # Process history.
        for agent_history in QLearningDecision.history_bank.values():
            # Apply temporal difference on banked data.
            for i in range(len(agent_history) - 2, -1, -1):
                agent_history[i].loss += self.discount_factor*agent_history[i + 1].loss

            # Add entry to q_table if loss is better than existing entry, or if observation has never been seen.
            for history_item in agent_history:
                existing_q_entry = self.q_table.get(history_item.observation)

                if existing_q_entry is None or existing_q_entry.loss > history_item.loss:
                    self.q_table[history_item.observation] = _QTableEntry(history_item.action_premise, history_item.loss)

        # Clear history bank.
        QLearningDecision.history_bank.clear()

        # Ui.
        sys.stdout.write("done\n")
        sys.stdout.flush()

    def _save_q_table_to_disk(self):
        """Saves the Q-Table to the file described by output_file_name"""
        # Don't even try to save if None
        if self.output_file_name is None:
            print("No output file name: Q-Learning data not saved.")
            return

        # Ui.
        sys.stdout.write("Saving Q-Learning data...")
        sys.stdout.flush()

        # Rename old .pkl file into a tmp while the new file is being written (crash safety).
        temp_file_name = self.output_file_name + ".tmp"
        if os.path.isfile(self.output_file_name):
            os.rename(self.output_file_name, temp_file_name)

        # write to file
        try:
            pickle.dump(self.q_table, open(self.output_file_name, "wb"), pickle.HIGHEST_PROTOCOL)
        except:
            raise Exception("An error occured while writing the Q-Table to the output file.")

        # remove old file
        if os.path.isfile(temp_file_name):
            os.remove(temp_file_name)

        # print messages
        if QLearningDecision.PRINT_DEBUG:
            self.printBestMoveDict()

        # Ui.
        sys.stdout.write("done\n")
        sys.stdout.flush()

    def _on_simulation_complete(self, simulation):
        """The callback that finalizes a simulation.

        Args:
            simulation (Simiulation): The Simulation.
        """
        self._update_q_table_from_history_bank()
        self._save_q_table_to_disk()

        
