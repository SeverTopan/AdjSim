#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# * A Flexible framework on top of which to simulate the activity of an
# * 'ecosystem'.
# * Enivronment is set up via a configuration script at the beginning of each
# * simulation that sets cycle schedules, resource locations, etc.
#
# Deisgned and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import sys
import re
import inspect
import random

#-------------------------------------------------------------------------------
# CLASS RESOURCE
#-------------------------------------------------------------------------------
class Resource():
    """docstring for Resource."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, name, blockedDuration = 0):
        self.environment = environment
        self.name = name
        self.blockedDuration = blockedDuration

#-------------------------------------------------------------------------------
# CLASS AGENT
#-------------------------------------------------------------------------------
class Agent(Resource):
    """docstring for Agent."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, abilities = {}, traits = {}):
        super(Agent, self).__init__()
        self.ability = abilities
        self.trait = traits

#-------------------------------------------------------------------------------
# CLASS ABILITY
#-------------------------------------------------------------------------------
class Ability(Resource):
    """docstring for Ability."""

    targets = {}

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, agent, targets, duration):
        super(Ability, self).__init__()
        self.agent = agent
        self.targets = targets
        self.duration = duration

# METHOD CAST
#-------------------------------------------------------------------------------
    def cast(self):
        # clear and obtain targets
        for target in self.targets:
            target.clear()
            target.obtain()

            if target.resource == None:
                return False

        # perform target effects and blocks
        for target in targets:
            target.performEffects
            target.performBlock

        return True


#-------------------------------------------------------------------------------
# CLASS TARGET
#-------------------------------------------------------------------------------
class Target():
    """docstring for Target."""

    conditions = []
    effects = []
    blockedDuration = 0;
    resource = None

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, environment, conditions, effects, blockedDuration):
        self.environment = environment
        self.conditions = conditions
        self.effects = effects
        self.blockedDuration = blockedDuration

# METHOD CLEAR
#-------------------------------------------------------------------------------
    def clear(self):
        self.resource = None

# METHOD MATCHED
#-------------------------------------------------------------------------------
    def matched(self):
        return (self.resource != None)

# METHOD OBTAIN
#-------------------------------------------------------------------------------
    def obtain(self):
        potentialTargets = {}

        # on no conditions, obtain random resource from environment
        if len(conditions) == 0:
            resource = environment.getTraitRandom()
        else:
            potentialTargets = potentialTargets \
                | environment.getTraitsOnCondition(condition[0])

        # intersect sets to narrow
        for condition in conditions:
            potentialTargets = potentialTargets \
                & environment.getTraitsOnCondition(condition)
            if len(potentialTargets) == 0:
                resource = None;
                return false;

        # for now, simply choose the first out of the list of targets
        resource = potentialTargets[0]

        return True

# METHOD PERFORM EFFECTS
#-------------------------------------------------------------------------------
    def performEffects(self):
        for effect in effects:
            effect(resource)

# METHOD PERFORM BLOCK
#-------------------------------------------------------------------------------
    def performBlock(self):
        resource.blockedDuration = blockedDuration


#-------------------------------------------------------------------------------
# CLASS TRAIT
#-------------------------------------------------------------------------------
class Trait(Resource):
    """docstring for Trait."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, agent, name, value):
        super(Trait, self).__init__()
        self.agent = agent
        self.name = name
        self.value = value
        self.isBlocked = isBlocked



#-------------------------------------------------------------------------------
# CLASS ENVIRONMENT
#-------------------------------------------------------------------------------
class Environment():
    """docstring for Environment."""

    agentList = {}
    time = None

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self):
        self.time = 0

# METHOD GET TRAIT RANDOM
#-------------------------------------------------------------------------------
    def getTraitRandom(self):
        selectedAgent = random.random() * len(self.agentList)
        selectedTrait = random.random() * len(selectedAgent.traits)

        return selectedAgent.traits[selectedTrait]

# METHOD GET TRAIT ON CONDITION
#-------------------------------------------------------------------------------
    def getTraitsOnCondition(self, condition):
        traitSet = {}

        for agent in self.agentList:
            for trait in agent.traits:
                if condition(trait):
                    traitSet.add(trait)

        return traitSet

#-------------------------------------------------------------------------------
# CLASS ADJECOSYSTEM
#-------------------------------------------------------------------------------
class AdjEcosystem:
    """docstring for AdjEcosystem."""

    environment = None

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, argv):
        self.environment = Environment()
        self.printWelcome()

        self.generateTestClasses()

# METHOD HORIZONTAL RULER
#-------------------------------------------------------------------------------
    @staticmethod
    def horizontalRuler(length):
        msg = ""
        for i in range(length):
            msg += "-"

        return msg

# METHOD PRINT WELCOME
#-------------------------------------------------------------------------------
    @staticmethod
    def printWelcome():
        welcomeMessage = "- AdjEcosystem -"

        print AdjEcosystem.horizontalRuler(len(welcomeMessage))
        print welcomeMessage
        print AdjEcosystemselfself.horizontalRuler(len(welcomeMessage))

# METHOD PARSE CONFIG FILE
#-------------------------------------------------------------------------------
    def parseConfigFile(self, argv):
        if len(argv) != 2:
            print "Invalid arguments - usage: python AdjEcosystem.py configfile"
            return False

        try:
            configFile = open(argv[1])
        except:
            print "Unable to open file", argv[1]
            return False

        print "Parsing Config file..."



        configData = configFile.read()
        agentMatches = re.findall('(agent:\\n(.+\\n)+)+?', configData)

        # unfinished, will add config file parsing functionality after core
        # functionality is ompletely implemented

        return

    def generateTestClasses(self):
        return


#-------------------------------------------------------------------------------
# MAIN EXECUTION SCRIPT
#-------------------------------------------------------------------------------
adjEcosystem = AdjEcosystem(sys.argv)
