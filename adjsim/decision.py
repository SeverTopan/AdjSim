
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan

# IMPORTS
# standard
import os
import sys
import re
import pickle
import random
import re

from . import utility

class DecisionMutableFloat(object):
    def __init__(self, min_val, max_val):
        self._value = float(max_val - min_val)
        self._min_val = min_val
        self._max_val = max_val

    @property
    def value(self):
        return self._value

    @property
    def min_val(self):
        return self._min_val

    @property
    def max_val(self):
        return self._max_val

    def _set_value(self, value):
        if value < self._min_val or value > self._max_val:
            raise ValueError

        self._value = value

class _DecisionMutablePremise(object):
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value

    def set(self, target):
        getattr(target, self.name)._set_value(self.value)

    def __repr__(self):
        return "(" + str(self.name) + " - " + str(self.value) + ")"


class _ActionPremiseIteration(object):
    def __init__(self, action_name=None, decision_mutables=None):
        self.action_name = action_name
        self.decision_mutables = [] if decision_mutables is None else decision_mutables

    def set_mutables(self, target):
        try:
            for decision_mutable in self.decision_mutables:
                decision_mutable.set(target)
        except:
            raise utility.MissingAttributeException

    def call_action(self, simulation, source):
        action = source.actions.get(self.action_name)
        if action is None:
            raise utility.MissingAttributeException
        
        action(simulation, source)

    def __repr__(self):
        return str(self.action_name) + " - " + str(self.decision_mutables)

class _ActionPremise(object):
    def __init__(self, iterations=None):
        self.iterations = [] if iterations is None else iterations
        

    def call(self, simulation, source):
        # Call all iterations.
        for iteration in self.iterations:
            # Check if complete.
            if source.step_complete:
                return

            # Setup and cast.
            iteration.set_mutables(source)
            iteration.call_action(simulation, source)

    def __repr__(self):
        return str(self.iterations)

class Decision(object):

    def __call__(self, simulation, source):
        raise NotImplementedError

class NoCastDecision(object):

    def __call__(self, simulation, source):
        return

class RandomSingleCastDecision(Decision):

    def __call__(self, simulation, source):
        # If no actions to choose from, skip.
        if len(source.actions) == 0:
            return

        # Randomly execute an action.
        try:
            action = random.choice(list(source.actions.values()))
            action(simulation, source)
        except TypeError:
            raise utility.InvalidActionException

class RandomRepeatedCastDecision(Decision):

    def __call__(self, simulation, source):
        # If no actions to choose from, skip.
        if len(source.actions) == 0:
            return

        # Randomly execute an action while the agent has not completed their timestep.
        while not source.step_complete:
            try:
                action = random.choice(list(source.actions.values()))
                action(simulation, source)
            except TypeError:
                raise utility.InvalidActionException

class FunctionalDecision(Decision):

    def __init__(self, perception, loss):
        self.perception = perception
        self.loss = loss

    def __call__(self, simulation, source):
        raise NotImplementedError

        
class _QLearningHistoryItem(object):
    def __init__(self, observation, action_premise, loss):
        self.observation = observation
        self.action_premise = action_premise
        self.loss = loss

class _QTableEntry(object):
    def __init__(self, action_premise, loss):
        self.action_premise = action_premise
        self.loss = loss

    def __repr__(self):
        return self.loss + " : " + self.action_premise.__repr__()

class QLearningDecision(FunctionalDecision):

    DEFAULT_IO_FILE_NAME = re.sub("\.py", ".qlearning.pkl", sys.argv[0])
    PRINT_DEBUG = False
    DEFAULT_DISCOUNT_FACTOR = 0.95
    DEFAULT_NONCONFORMITY_FACTOR = 0.3

    history_bank = {}

    def __init__(self, perception, loss, 
                 input_file_name=DEFAULT_IO_FILE_NAME, output_file_name=DEFAULT_IO_FILE_NAME,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR, nonconformity_factor=DEFAULT_NONCONFORMITY_FACTOR):
        super().__init__(perception, loss)

        # Initialize members.
        self.q_table = {}
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.discount_factor = discount_factor
        self.nonconformity_factor = nonconformity_factor

        # Load q_table
        self._load_q_table_from_disk()


    def _load_q_table_from_disk(self):
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
        for observation, item in self.q_table.items():
            print("   ", observation, " > ", item.action_premise)

    def __call__(self, simulation, source):
        # Observe environment.
        observation = None
        try:
            observation = self.perception(simulation, source)
        except TypeError:
            raise utility.InvalidPerceptionException

        # Check for a known action premise.
        q_table_entry = self.q_table.get(observation)
        action_premise = q_table_entry.action_premise if not q_table_entry is None else None

        # Cast action.
        # The random action will still be called even if a q_table entry is found.
        # This happens with a probability represented by the nonconformity_factor.
        if action_premise is None or random.random() < self.nonconformity_factor:
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
                except TypeError:
                    raise utility.InvalidActionException

                # Save action premise.
                action_premise.iterations.append(action_premise_iteration)

        else:
            # Call the action premise.
            action_premise.call(simulation, source)

        # Obtain current loss.
        current_loss = None
        try:
            current_loss = self.loss(simulation, source)
        except TypeError:
            raise utility.InvalidLossException

        # Bank history.
        history_item = _QLearningHistoryItem(observation, action_premise, current_loss)
        agent_history = QLearningDecision.history_bank.get(source.id)
        if agent_history is None:
            QLearningDecision.history_bank[source.id] = [history_item]
        else:
            QLearningDecision.history_bank[source.id].append(history_item)

    def _update_q_table_from_history_bank(self):
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
        self._update_q_table_from_history_bank()
        self._save_q_table_to_disk()

        
