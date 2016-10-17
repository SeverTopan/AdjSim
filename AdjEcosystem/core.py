#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
from environment import *
from tests import *
from graphics import *
import time

#-------------------------------------------------------------------------------
# CLASS ADJECOSYSTEM
#-------------------------------------------------------------------------------
class AdjEcosystem(object):
    """docstring for AdjEcosystem."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, argv):
        self.environment = Environment()
        self.graphics = Graphics()
        AdjEcosystem.printWelcome()


# METHOD PRINT WELCOME
#-------------------------------------------------------------------------------
    @staticmethod
    def printWelcome():
        welcomeMessage = "- AdjEcosystem -"

        print(" ".ljust(len(welcomeMessage), "-"))
        print(welcomeMessage)
        print(" ".ljust(len(welcomeMessage), "-"))

# METHOD SIMULATE
#-------------------------------------------------------------------------------
    def simulate(self, numTimesteps):
        # print header
        self.environment.printSnapshot()
        print("Simulating: ", numTimesteps, " time steps")

        # draw initial frame
        self.graphics.update(self.environment.agentSet)
        time.sleep(1)

        # run simulation steps for num time steps
        for timeStep in range(numTimesteps):
            self.environment.executeAbilities()
            self.environment.executeTimestep()
            self.environment.cleanupNonExistentAgents()

            self.graphics.update(self.environment.agentSet)
            time.sleep(1)


        # print footer
        print("...Simulation Complete")
        self.environment.printSnapshot()

# METHOD PARSE CONFIG FILE
#-------------------------------------------------------------------------------
    def parseConfigFile(self, argv):
        if len(argv) != 2:
            print("Invalid arguments - usage: python AdjEcosystem.py configfile")
            return False

        try:
            configFile = open(argv[1])
        except:
            print("Unable to open file", argv[1])
            return False

        print("Parsing Config file...")



        configData = configFile.read()
        agentMatches = re.findall('(agent:\\n(.+\\n)+)+?', configData)

        # unfinished, will add config file parsing functionality after core
        # functionality is completely implemented

        return
