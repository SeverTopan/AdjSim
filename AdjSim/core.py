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
import sys, os

#-------------------------------------------------------------------------------
# CLASS ADJSIM
#-------------------------------------------------------------------------------
class AdjSim(object):
    """docstring for AdjSim."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, argv, graphicsEnabled):
        AdjSim.printWelcome()
        os.remove('debug.log')
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

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
        tests.generateTestClasses_bacteriaYogurt(environment)
        # tests.generateTestClasses_planets(environment)
        environment.simulate(1000, thread)
        time.sleep(20)


# METHOD PRINT WELCOME
#-------------------------------------------------------------------------------
    @staticmethod
    def printWelcome():
        welcomeMessage = "- AdjSim -"

        print("-".rjust(len(welcomeMessage), "-"))
        print(welcomeMessage)
        print("-".rjust(len(welcomeMessage), "-"))



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
