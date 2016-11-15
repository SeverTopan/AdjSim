#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
from environment import *
from tests import *
from graphics import *
import time
import logging
import re
import sys, os

#-------------------------------------------------------------------------------
# CLASS ADJSIM
#-------------------------------------------------------------------------------
class AdjSim(object):
    """docstring for AdjSim."""

    environmentGenerationFunction = None
    environmentGenerationIdentifierArg = None
    simulationLength = None

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, argv, graphicsEnabled):
        AdjSim.printWelcome()

        # setup debug logging
        logPath = AdjSim.getLogPath()
        if os.path.isfile(logPath):
            os.remove(logPath)
        logging.basicConfig(filename=logPath, level=logging.DEBUG)

        # check arguments
        if not AdjSim.parseArgs(argv):
            return

        # perform threading initialization for graphics
        if graphicsEnabled:
            self.qApp = QtGui.QApplication(argv)
            self.view = AdjGraphicsView(self.qApp.desktop().screenGeometry())
            self.thread = AdjThread(self.qApp)
            self.thread.finished.connect(self.qApp.exit)
            self.qApp.connect(self.thread, self.thread.signal, self.view.update)
            self.thread.start()
            sys.exit(self.qApp.exec_())
        else:
            self.environment = Environment()
            AdjSim.run(self.environment)

# METHOD RUN
#-------------------------------------------------------------------------------
    @staticmethod
    def run(environment, thread=None):
        if AdjSim.environmentGenerationIdentifierArg:
            AdjSim.environmentGenerationFunction(environment, AdjSim.environmentGenerationIdentifierArg)
        else:
            AdjSim.environmentGenerationFunction(environment)

        environment.simulate(AdjSim.simulationLength, thread)
        time.sleep(20)

# METHOD GET LOG PATH
#-------------------------------------------------------------------------------
    @staticmethod
    def getLogPath():
        debugPath = os.path.realpath(__file__)
        debugPath = re.sub('core\.py', '', debugPath)
        debugPath += 'debug.log'
        return debugPath


# METHOD PRINT WELCOME
#-------------------------------------------------------------------------------
    @staticmethod
    def printWelcome():
        welcomeMessage = "- AdjSim -"

        print("-".rjust(len(welcomeMessage), "-"))
        print(welcomeMessage)
        print("-".rjust(len(welcomeMessage), "-"))

# METHOD INVALID ARGS
#-------------------------------------------------------------------------------
    @staticmethod
    def printInvalidArgs():
        print('Invalid Arguments - Usage: python <AdjSim directory> <simulation descriptor> <simulation length>')
        print('Currently accepted simulation descriptors:')
        print('     - demo_bacteria')
        print('     - demo_planets_earth')
        print('     - demo_planets_jupiter')


# METHOD PARSE ARGS
#-------------------------------------------------------------------------------
    @staticmethod
    def parseArgs(argv):
        if len(argv) < 3 or len(argv) > 3:
            AdjSim.printInvalidArgs()
            return False
        else:
            if argv[1] == 'demo_bacteria':
                AdjSim.environmentGenerationFunction = tests.generateTestClasses_bacteriaYogurt
            elif argv[1] == 'demo_planets_earth':
                AdjSim.environmentGenerationFunction = tests.generateTestClasses_planets
                AdjSim.environmentGenerationIdentifierArg = 'earth'
            elif argv[1] == 'demo_planets_jupiter':
                AdjSim.environmentGenerationFunction = tests.generateTestClasses_planets
                AdjSim.environmentGenerationIdentifierArg = 'jupiter'
            else:
                AdjSim.printInvalidArgs()
                return False

            AdjSim.simulationLength = int(argv[2])

            return True

# METHOD PARSE CONFIG FILE
#-------------------------------------------------------------------------------
    def parseConfigFile(self, argv):
        if len(argv) != 2:
            print("Invalid arguments - usage: python AdjSim.py configfile")
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
