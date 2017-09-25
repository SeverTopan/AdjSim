
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan

# IMPORTS
# standard
import os
import sys
import re
import pickle
import random

from . import utility

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