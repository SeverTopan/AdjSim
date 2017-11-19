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
import copy
import math

# Third party.
from matplotlib import pyplot
import numpy as np

# Local.
from . import utility
from . import callback

class DecisionMutableValue(object):
    """Base class for decision mutable objects.

    A decision mutable value represents a value that a particular decision module will try to optimize for.
    They are used to parameterize functions within AdjSim's definition of an 'action'.
    """
    pass

class DecisionMutableBool(DecisionMutableValue):
    """Contains a boolean that the decision module will modify.

    A decision mutable bool represents a value that a particular decision module will try to optimize for.
    perturbation_scale relates to the probability the locus will flip its value.
    """

    DEFAULT_PERTURBATION_SCALE = 0.3

    def __init__(self, perturbation_scale=DEFAULT_PERTURBATION_SCALE):
        super().__init__()
        self._value = None
        self._perturbation_scale = perturbation_scale

    @property
    def value(self):
        """bool: Obtain the value."""
        return self._value

    @property
    def perturbation_scale(self):
        """float: Obtain the perturbation scale."""
        return self._perturbation_scale

    def _set_value(self, value):
        """Private setter for use by decision modules."""
        self._value = bool(value)

    def _set_value_random(self):
        """Private function to assign value based on uniform random distribution inside range."""
        self._value = bool(random.getrandbits(1))

    def _perturb_locally(self):
        """Private function to assign value based local perturbation to the current value."""
        self._perturb_around_locus(self._value)

    def _perturb_around_locus(self, locus):
        """Private function to assign value based local perturbation to the given parameter."""
        self._set_value(not bool(locus) if random.random() < self._perturbation_scale else locus)
        


class DecisionMutableFloat(DecisionMutableValue):
    """Contains a bounded float that the decision module will modify.

    A decision mutable float represents a value that a particular decision module will try to optimize for.
    This float must be given viable bounds between which the decision module will try to find an optimal 
    value to fulfill its loss function.

    Bounds are inclusive: value in [min_val, max_val].
    perturbation_scale relates to the scale of the np.random.normal.
    """

    DEFAULT_PERTURBATION_SCALE = 1.0

    def __init__(self, min_val, max_val, perturbation_scale=DEFAULT_PERTURBATION_SCALE):
        super().__init__()

        self._value = None
        self._min_val = float(min_val)
        self._max_val = float(max_val)
        self._perturbation_scale = perturbation_scale

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

    @property
    def perturbation_scale(self):
        """float: Obtain the perturbation scale."""
        return self._perturbation_scale

    def _set_value(self, value):
        """Private setter for use by decision modules."""
        if value < self._min_val or value > self._max_val:
            raise ValueError

        self._value = float(value)

    def _set_value_random(self):
        """Private function to assign value based on uniform random distribution inside range."""
        self._value = random.uniform(self.min_val, self.max_val)

    def _perturb_locally(self):
        """Private function to assign value based local perturbation to the current value."""
        self._perturb_around_locus(self._value)

    def _perturb_around_locus(self, locus):
        """Private function to assign value based local perturbation to the given parameter."""
        self._perturb_value_gaussian(locus)

    def _perturb_value_gaussian(self, locus):
        """Private function to assign value based on a gaussian perturbation."""
        self._set_value(np.clip(np.random.normal(locus, self._perturbation_scale), \
            self.min_val, self.max_val))


class DecisionMutableInt(DecisionMutableValue):
    """Contains a bounded integer that the decision module will modify.

    A decision mutable integer represents a value that a particular decision module will try to optimize for.
    This integer must be given viable bounds between which the decision module will try to find an optimal 
    value to fulfill its loss function.

    Bounds are inclusive: value in [min_val, max_val].    
    perturbation_scale relates to the scale of the np.random.normal.
    """

    DEFAULT_PERTURBATION_SCALE = 1.0

    def __init__(self, min_val, max_val, perturbation_scale=DEFAULT_PERTURBATION_SCALE):
        super().__init__()

        self._value = None
        self._min_val = int(min_val)
        self._max_val = int(max_val)
        self._perturbation_scale = perturbation_scale

    @property
    def value(self):
        """int: Obtain the value."""
        return self._value

    @property
    def min_val(self):
        """int: Obtain the minimum bound."""
        return self._min_val

    @property
    def max_val(self):
        """int: Obtain the maximum bound."""
        return self._max_val

    @property
    def perturbation_scale(self):
        """float: Obtain the perturbation scale."""
        return self._perturbation_scale

    def _set_value(self, value):
        """Private setter for use by decision modules."""
        if value < self._min_val or value > self._max_val:
            raise ValueError

        self._value = int(value)

    def _set_value_random(self):
        """Private function to assign value based on uniform random distribution inside range."""
        self._value = random.randint(self.min_val, self.max_val)

    def _perturb_locally(self):
        """Private function to assign value based local perturbation to the current value."""
        self._perturb_around_locus(self._value)

    def _perturb_around_locus(self, locus):
        """Private function to assign value based local perturbation to the given parameter."""
        self._perturb_value_gaussian(locus)

    def _perturb_value_gaussian(self, locus):
        """Private function to assign value based on a gaussian perturbation."""
        self._set_value(np.clip(round(np.random.normal(locus, self._perturbation_scale)), \
            self.min_val, self.max_val))


class ArrayConstraint(object):
    """Abstract base class for array constraints."""
    def satisfies(self, value):
        raise NotImplementedError


class PositiveSumConstraint(ArrayConstraint):
    """Constrain a decision-mutable array so that all elements sum to a given value. 
    All elements will be positive.
    """
    def __init__(self, sum_constraint):
        if sum_constraint is None:
            raise ValueError("Sum may not be None.")

        if math.isclose(sum_constraint, 0):
            raise ValueError("Sum may not be 0.")

        self.sum = sum_constraint

    def satisfies(self, value):
        return math.isclose(np.sum(value), self.sum)


class RangeConstraint(ArrayConstraint):
    """Constrain a decision-mutable array so that all elements fall in a given range."""
    def __init__(self, min_val, max_val):
        if min_val is None or max_val is None:
            raise ValueError("Bounds may not be None.")

        self.min_val = min_val
        self.max_val = max_val

    def satisfies(self, value):
        return (value >= self.min_val).all() and (value <= self.max_val).all()


class DecisionMutableBoolArray(DecisionMutableValue):
    """Contains an array of booleans that the decision module will modify.

    A decision mutable bool array represents a value that a particular decision module will try to optimize for.
    perturbation_scale relates to the probability the locus will flip its value.
    """

    DEFAULT_PERTURBATION_SCALE = 1.0

    def __init__(self, shape, perturbation_scale=DEFAULT_PERTURBATION_SCALE):
        super().__init__()
        if not np.any(shape):
            raise ValueError("Invalid shape.")

        self._shape = tuple(shape)
        self._value = np.zeros(self._shape, dtype=np.bool_)
        self._perturbation_scale = perturbation_scale

    @property
    def value(self):
        """np.array: Obtain the value."""
        return self._value

    @property
    def shape(self):
        """np.array: Obtain the array shape."""
        return self._shape

    @property
    def perturbation_scale(self):
        """float: Obtain the perturbation scale."""
        return self._perturbation_scale

    def _set_value(self, value):
        """Private setter for use by decision modules."""
        if not isinstance(value, np.ndarray) or value.dtype != np.bool_:
            raise TypeError
            
        if value.shape != self._shape:
            raise ValueError

        self._value = value

    def _set_value_random(self):
        """Private function to assign random array value based on constraints."""
        self._value = np.random.random(self._shape) > 0.5

    def _perturb_locally(self):
        """Private function to assign value based local perturbation to the current value."""
        self._perturb_around_locus(self._value)

    def _perturb_around_locus(self, locus):
        """Private function to assign value based local perturbation to the given parameter."""
        flip = np.random.random(self._shape) < self._perturbation_scale
        self._set_value(np.logical_xor(locus, flip))


class DecisionMutableIntArray(DecisionMutableValue):
    """Contains an integer array that the decision module will modify.

    A decision mutable integer array represents a value that a particular decision module will try to optimize for.
    This integer must be given viable constraints between which the decision module will try to find an optimal 
    value to fulfill its loss function.

    A constraint must be specified. SumContraint is not supported.
    perturbation_scale relates to the scale of the np.random.normal.
    """

    DEFAULT_PERTURBATION_SCALE = 1.0

    def __init__(self, shape, constraint, perturbation_scale=DEFAULT_PERTURBATION_SCALE):
        super().__init__()

        # Error check constraints.
        if not issubclass(type(constraint), ArrayConstraint):
            raise ValueError("Invalid constraint.")

        if not np.any(shape):
            raise ValueError("Invalid shape.")

        self._constraint = copy.copy(constraint)
        self._shape = tuple(shape)
        self._value = np.zeros(self._shape, dtype=np.int_)
        self._perturbation_scale = perturbation_scale

    @property
    def value(self):
        """np.array: Obtain the value."""
        return self._value

    @property
    def constraint(self):
        """ArrayContraint: Obtain a copy of the constraint."""
        return copy.copy(self._constraint)

    @property
    def shape(self):
        """np.array: Obtain the array shape."""
        return self._shape

    @property
    def perturbation_scale(self):
        """float: Obtain the perturbation scale."""
        return self._perturbation_scale

    def _set_value(self, value):
        """Private setter for use by decision modules."""
        if not isinstance(value, np.ndarray) or value.dtype != np.int_:
            raise TypeError
            
        if value.shape != self._shape or not self.constraint.satisfies(value):
            raise ValueError

        self._value = value

    def _set_value_random(self):
        """Private function to assign random array value based on constraints."""
        
        if isinstance(self._constraint, RangeConstraint):
            self._value = np.random.randint(self._constraint.min_val, self._constraint.max_val, size=self._shape)

        else:
            raise ValueError("Invalid constraint type.")

    def _perturb_locally(self):
        """Private function to assign value based local perturbation to the current value."""
        self._perturb_around_locus(self._value)

    def _perturb_around_locus(self, locus):
        """Private function to assign value based local perturbation to the given parameter."""
        if isinstance(self._constraint, RangeConstraint):
            self._perturb_value_gaussian_range_constraint(locus)

        else:
            raise ValueError("Invalid constraint type.")

    def _perturb_value_gaussian_range_constraint(self, locus):
        """Private function to assign value based on a gaussian perturbation."""
        self._set_value(np.clip(np.random.normal(locus, self._perturbation_scale).astype(np.int), \
            self._constraint.min_val, self._constraint.max_val))

class DecisionMutableFloatArray(DecisionMutableValue):
    """Contains an float array that the decision module will modify.

    A decision mutable float array represents a value that a particular decision module will try to optimize for.
    This float must be given viable constraints between which the decision module will try to find an optimal 
    value to fulfill its loss function.

    A constraint must be specified. 

    perturbation_scale relates to the scale of the np.random.normal.
    """

    DEFAULT_PERTURBATION_SCALE = 1.0
    
    def __init__(self, shape, constraint, perturbation_scale=DEFAULT_PERTURBATION_SCALE):
        super().__init__()

        # Error check constraints.
        if not issubclass(type(constraint), ArrayConstraint):
            raise ValueError("Invalid constraint.")

        if not np.any(shape):
            raise ValueError("Invalid shape.")

        self._constraint = copy.copy(constraint)
        self._shape = tuple(shape)
        self._value = np.zeros(self._shape, dtype=np.float_)
        self._perturbation_scale = perturbation_scale

    @property
    def value(self):
        """np.array: Obtain the value."""
        return self._value

    @property
    def constraint(self):
        """ArrayContraint: Obtain a copy of the constraint."""
        return copy.copy(self._constraint)

    @property
    def shape(self):
        """np.array: Obtain the array shape."""
        return self._shape

    @property
    def perturbation_scale(self):
        """float: Obtain the perturbation scale."""
        return self._perturbation_scale

    def _set_value(self, value):
        """Private setter for use by decision modules."""
        if not isinstance(value, np.ndarray) or value.dtype != np.float_:
            raise TypeError

        if value.shape != self._shape  or not self.constraint.satisfies(value):
            raise ValueError

        self._value = value

    def _set_value_random(self):
        """Private function to assign random array value based on constraints."""
        
        if isinstance(self._constraint, RangeConstraint):
            self._value = np.random.uniform(self._constraint.min_val, self._constraint.max_val, size=self._shape)

        elif isinstance(self._constraint, PositiveSumConstraint):
            temp = np.random.random(size=self._shape)
            self._value = temp/np.sum(temp)*self._constraint.sum

        else:
            raise ValueError("Invalid constraint type.")

    def _perturb_locally(self):
        """Private function to assign value based local perturbation to the current value."""
        self._perturb_around_locus(self._value)

    def _perturb_around_locus(self, locus):
        """Private function to assign value based local perturbation to the given parameter."""

        if isinstance(self._constraint, RangeConstraint):
            self._perturb_value_gaussian_range_constraint(locus)

        elif isinstance(self._constraint, PositiveSumConstraint):
            self._perturb_value_gaussian_sum_constraint(locus)

        else:
            raise ValueError("Invalid constraint type.")

    def _perturb_value_gaussian_range_constraint(self, locus):
        """Private function to assign value based on a gaussian perturbation."""
        self._set_value(np.clip(np.random.normal(locus, self._perturbation_scale), \
            self._constraint.min_val, self._constraint.max_val))

    def _perturb_value_gaussian_sum_constraint(self, locus):
        """Private function to assign value based on a gaussian perturbation."""
        temp = np.random.normal(np.zeros(self._shape), self._perturbation_scale)
        perturbation = temp - np.sum(temp)/temp.size
        self._set_value(locus + perturbation)


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
        return "\n(" + repr(self.name) + " - " + repr(self.value) + ")"


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
        return "\n" + repr(self.action_name) + " - " + repr(self.decision_mutables)

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
        return repr(self.iterations)

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
        decision_mutable_names = [d for d in dir(source) if issubclass(type(getattr(source, d)), DecisionMutableValue)]
        for decision_mutable_name in decision_mutable_names:
            decision_mutable = getattr(source, decision_mutable_name)
            decision_mutable._set_value_random()

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
            decision_mutable_names = [d for d in dir(source) if issubclass(type(getattr(source, d)), DecisionMutableValue)]
            for decision_mutable_name in decision_mutable_names:
                decision_mutable = getattr(source, decision_mutable_name)
                decision_mutable._set_value_random()

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
        return repr(self.loss) + " : " + repr(self.action_premise)

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
    DEFAULT_DISCOUNT_FACTOR = 0.95
    DEFAULT_NONCONFORMITY_FACTOR = 0.3

    print_debug = False

    def __init__(self, perception, loss, simulation,
                 input_file_name=DEFAULT_IO_FILE_NAME, 
                 output_file_name=DEFAULT_IO_FILE_NAME,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR, 
                 nonconformity_probability=DEFAULT_NONCONFORMITY_FACTOR):
        super().__init__(perception, loss)

        # Initialize members.
        self.q_table = {}
        self.history_bank = {}
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.discount_factor = discount_factor
        self.nonconformity_probability = nonconformity_probability
        self.completion_callback =  callback.SingleParameterCallback()

        # Private members.
        self._tentative_history_bank = {}
        self._simulation = simulation

        # Load q_table
        self._load_q_table_from_disk()

        # Register callbacks.
        self._simulation.callbacks.simulation_complete.register(self._on_simulation_complete)
        self._simulation.callbacks.agent_removed.register(self._on_agent_removal)

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
        if QLearningDecision.print_debug:
            self.print_q_table()
        sys.stdout.write("done\n")
        sys.stdout.flush()

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
        # Obtain previous step's loss for the given agent.
        # Loss is calculated for every antecedent step right before the subsequent action is made by a given agent.
        self._save_loss(source)
        
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
        if action_premise is None:
            action_premise = self._generate_unprecedented_action_premise(source)

        elif random.random() < self.nonconformity_probability:
            action_premise = self._generate_nonconformative_action_premise(source, action_premise)

        else:
            # Call the action premise.
            action_premise.call(simulation, source)

        # Bank history.
        history_item = _QLearningHistoryItem(observation, action_premise, None)
        agent_history = self.history_bank.get(source.id)
        if agent_history is None:
            self.history_bank[source.id] = [history_item]
        else:
            self.history_bank[source.id].append(history_item)

    def _generate_unprecedented_action_premise(self, source):
        """Generate, invoke and return an action premise for the case where no known
        prior instance of a given observation has been seen by the QLearning module.
        """
        return self._generate_new_random_action_premise(source)

    def _generate_nonconformative_action_premise(self, source, existing_action_premise):
        """Generate, invoke and return an action premise for the case we invoke non-conformity."""
        return self._generate_new_random_action_premise(source)        

    def _generate_new_random_action_premise(self, source):
        """Generate, invoke and return a random new action premise.

        Here we essentially perorm a RandomRepeatedCast decision, and return the 
        resulting action premise.
        """
        # Prepare action premise.
        action_premise = _ActionPremise()

        # This is essentially a RandomRepeatedCast.
        while not source.step_complete:
            action_premise_iteration = _ActionPremiseIteration()

            # Set decision mutable values to random values, save to action premise.
            decision_mutable_names = [d for d in dir(source) if issubclass(type(getattr(source, d)), DecisionMutableValue)]
            for decision_mutable_name in decision_mutable_names:
                decision_mutable = getattr(source, decision_mutable_name)
                decision_mutable._set_value_random()

                action_premise_iteration.decision_mutables.append(_DecisionMutablePremise(decision_mutable_name, decision_mutable.value))

            # Cast fallback decision, save to action premise.
            try:
                identifier, action = random.choice(list(source.actions.items()))
                action(self._simulation, source)
                action_premise_iteration.action_name = identifier
            except:
                raise utility.ActionException

            # Save action premise.
            action_premise.iterations.append(action_premise_iteration)

        return action_premise

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
        num_updated = 0
        for agent_history in self.history_bank.values():
            # Apply temporal difference on banked data.
            for i in range(len(agent_history) - 2, -1, -1):
                agent_history[i].loss += self.discount_factor*agent_history[i + 1].loss

            # Add entry to q_table if loss is better than existing entry, or if observation has never been seen.
            for history_item in agent_history:
                existing_q_entry = self.q_table.get(history_item.observation)

                if existing_q_entry is None or existing_q_entry.loss > history_item.loss:
                    num_updated += 1
                    self.q_table[history_item.observation] = _QTableEntry(history_item.action_premise, history_item.loss)

        # Trigger callback before history bank is cleared.
        self.completion_callback(self.history_bank)

        # Clear history bank.
        self.history_bank.clear()

        # Ui.
        sys.stdout.write("done - {} entries updated\n".format(num_updated))
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
        if QLearningDecision.print_debug:
            self.print_q_table()

        # Ui.
        sys.stdout.write("done\n")
        sys.stdout.flush()

    def _on_simulation_complete(self, simulation):
        """The callback that finalizes a simulation.

        Args:
            simulation (Simiulation): The Simulation.
        """
        # Update final losses.
        for agent in simulation.agents:
            if agent.decision is self:
                self._save_loss(agent)

        # Save all final losses.
        self._update_q_table_from_history_bank()
        self._save_q_table_to_disk()

    def _save_loss(self, source):
        """Saves the loss into the antecedent history item.

        Args:
            Source (Agent): The source agent.
        """
        current_loss = None
        try:
            current_loss = self.loss(self._simulation, source)
        except:
            raise utility.LossException

        entry = self.history_bank.get(source.id)
        if not entry is None: # This occurs during the first timestep.
            entry[-1].loss = current_loss

    def _on_agent_removal(self, agent):
        """The callback that saves an agent's loss after it is removed from the simulation.

        Args:
            agent (Agent): The Agent.
        """
        if agent.decision is self:
            self._save_loss(agent)

    def print_q_table(self):
        """Debug printing of the Q-Table"""
        for observation, item in self.q_table.items():
            print("   ", observation, " > ", item)


class PerturbativeQLearningDecision(QLearningDecision):
    """A decision module based on Q-Learning.

    This module employs Q-Learning (https://en.wikipedia.org/wiki/Q-learning), a reinforcement
    learning technique, to incrementally enhance its performance as measured by the provided loss
    function. Over many simulations, the performance of the agent will be increased.

    The difference between this and the canonical QLearning decision module is the non-conformity behaviour.
    Non-conforming calls will perturb existing action premises instead of generating completely new ones

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

    class Config(object):
        """Configuration object for Perturbative Q-Learning. There are 3 types of mutually-inclusive
        perturbations that can take place. The values contained within this object represent the probability
        that the given perturbation will take place. 

        reorder_probability (float): Probability that the existing action sequence will be reordered.
        ignore_probability (float): Proability that existing actions will be removed from the sequence.
        local_perturbation_probability (float): Probability that local pertrurbations will be induced upon the
            individual elements of the existing action sequence.
        """

        DEFAULT_REORDER_PROBABILITY = 0.2
        DEFAULT_IGNORE_PROBABILITY = 0.3
        DEFAULT_LOCAL_PERTURBATION_PROBABILITY = 0.7

        def __init__(self, reorder_probability=DEFAULT_REORDER_PROBABILITY, 
                     ignore_proabability=DEFAULT_IGNORE_PROBABILITY, 
                     local_perturbation_probability=DEFAULT_LOCAL_PERTURBATION_PROBABILITY):
                    
            self._reorder_probability = reorder_probability
            self._ignore_proabability = ignore_proabability
            self._local_perturbation_probability = local_perturbation_probability

        @property
        def reorder_probability(self):
            """float: obtain the probability that reordering will take place."""
            return self._reorder_probability

        @reorder_probability.setter
        def reorder_probability(self, value):
            val = float(value)
            if val > 1.0 or val < 0:
                raise ValueError("Value must be between 0 and 1")

            self._reorder_probability = val

        @property
        def ignore_probability(self):
            """float: obtain the probability that existing actions will be ignored."""
            return self._ignore_proabability

        @ignore_probability.setter
        def ignore_probability(self, value):
            val = float(value)
            if val > 1.0 or val < 0:
                raise ValueError("Value must be between 0 and 1")

            self._ignore_proabability = val

        @property
        def local_perturbation_probability(self):
            """float: obtain the probability that existing actions will be locally perturbed."""
            return self._local_perturbation_probability

        @local_perturbation_probability.setter
        def local_perturbation_probability(self, value):
            val = float(value)
            if val > 1.0 or val < 0:
                raise ValueError("Value must be between 0 and 1")

            self._local_perturbation_probability = val


    def __init__(self, perception, loss, simulation,
                 input_file_name=QLearningDecision.DEFAULT_IO_FILE_NAME, 
                 output_file_name=QLearningDecision.DEFAULT_IO_FILE_NAME,
                 discount_factor=QLearningDecision.DEFAULT_DISCOUNT_FACTOR, 
                 nonconformity_probability=QLearningDecision.DEFAULT_NONCONFORMITY_FACTOR,
                 perturbation_config=Config()):
        super().__init__(perception, loss, simulation, input_file_name, output_file_name, 
                         discount_factor, nonconformity_probability)
        self._config = perturbation_config

    @property
    def config(self):
        """Config: obtain the perturbation configuration object."""
        return self._config

    @config.setter
    def config(self, value):
        if not isinstance(value, Config):
            raise TypeError("Value must be of type PerturbativeQLearningDecision.Config")

        self._config = value

    def _generate_nonconformative_action_premise(self, source, existing_action_premise):
        """Generate, invoke and return an action premise for the case we invoke non-conformity."""
        # Prepare action premise.
        action_premise = copy.copy(existing_action_premise)

        # Ignore-type perturbation.
        ignoration_array = np.random.random((len(action_premise.iterations),)) < self._config.ignore_probability
        action_premise.iterations = [e for i, e in enumerate(action_premise.iterations) if not ignoration_array[i]]

        # Reorder-type perturbation.
        if random.random() < self._config.reorder_probability:
            random.shuffle(action_premise.iterations)

        # Cast existing action premise.
        iteration_index = 0
        while not source.step_complete and iteration_index < len(action_premise.iterations):
            # Set and locally perturb decision mutables.
            action_premise.iterations[iteration_index].set_mutables(source)
            decision_mutable_names = [d for d in dir(source) if issubclass(type(getattr(source, d)), DecisionMutableValue)]
            for decision_mutable_name in decision_mutable_names:
                decision_mutable = getattr(source, decision_mutable_name)
                decision_mutable._perturb_locally()

            # Invoke action.
            action_premise.iterations[iteration_index].call_action(self._simulation, source)

            iteration_index += 1

        # Call further actions.
        while not source.step_complete:
            action_premise_iteration = _ActionPremiseIteration()

            # Set decision mutable values to random values, save to action premise.
            decision_mutable_names = [d for d in dir(source) if issubclass(type(getattr(source, d)), DecisionMutableValue)]
            for decision_mutable_name in decision_mutable_names:
                decision_mutable = getattr(source, decision_mutable_name)
                decision_mutable._set_value_random()

                action_premise_iteration.decision_mutables.append(_DecisionMutablePremise(decision_mutable_name, decision_mutable.value))

            # Cast fallback decision, save to action premise.
            try:
                identifier, action = random.choice(list(source.actions.items()))
                action(self._simulation, source)
                action_premise_iteration.action_name = identifier
            except:
                raise utility.ActionException

            # Save action premise.
            action_premise.iterations.append(action_premise_iteration)

        return action_premise