#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
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

    simulationLength = None
    graphicsEnabled = None
    scriptPath = None

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, argv):
        AdjSim.printWelcome()

        # setup debug logging
        logPath = AdjSim.getLogPath()
        if os.path.isfile(logPath):
            os.remove(logPath)
        logging.basicConfig(filename=logPath, level=logging.DEBUG)
        logging.disable(logging.CRITICAL)

        # check arguments
        if not AdjSim.parseArgs(argv):
            return

        # perform threading initialization for graphics
        if AdjSim.graphicsEnabled:
            self.updateSemaphore = QtCore.QSemaphore(0)

            self.qApp = QtGui.QApplication(argv)
            self.view = AdjGraphicsView(self.qApp.desktop().screenGeometry(), self.updateSemaphore)
            self.thread = AdjThread(self.qApp, self.updateSemaphore)

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

        exec(open(AdjSim.scriptPath).read(), locals())

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
        print('Invalid Arguments - Usage: python <AdjSim directory> <options> <simulation script> <simulation length>')
        print('For demo scripts, please see AdjSim/demo')
        print('Options: \n     -s : Suppress graphical simulation representation')

# METHOD PARSE ARGS
#-------------------------------------------------------------------------------
    @staticmethod
    def parseArgs(argv):
        simLength = None

        if len(argv) == 3:
            AdjSim.graphicsEnabled = True
            AdjSim.scriptPath = argv[1]
            simLength = argv[2]
        elif len(argv) == 4:
            if argv[1] == '-s':
                AdjSim.graphicsEnabled = False
            else:
                AdjSim.printInvalidArgs()
                return False
            AdjSim.scriptPath = argv[2]
            simLength = argv[3]
        else:
            AdjSim.printInvalidArgs()
            return False

        # parse simulation script
        if not os.path.isfile(AdjSim.scriptPath):
            AdjSim.printInvalidArgs()
            return False

        # parse simulation length
        try:
            AdjSim.simulationLength = int(simLength)
        except:
            AdjSim.printInvalidArgs()
            return False

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
