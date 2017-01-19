#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
# standard
import time
import logging
import re
import sys
import os

# third party
from PyQt4 import QtGui, QtCore
from matplotlib import pyplot

# local
from . import Graphics
from . import Simulation
from . import Intelligence

#-------------------------------------------------------------------------------
# CLASS ADJSIM
#-------------------------------------------------------------------------------
class AdjSim(object):
    """docstring for AdjSim."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, argv=None):
        AdjSim.printWelcome()

        # setup debug logging
        logPath = AdjSim.getLogPath()
        if os.path.isfile(logPath):
            os.remove(logPath)
        logging.basicConfig(filename=logPath, level=logging.DEBUG)
        logging.disable(logging.CRITICAL)

        # init environment
        self.environment = Simulation.Environment()

        # pyplot multitheading
        AdjSim.pyplotMultithreadingHack()

# METHOD RUN
#-------------------------------------------------------------------------------
    @staticmethod
    def run(environment, thread=None):
        environment.simulate(AdjSim.simulationLength, thread)

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


# METHOD PYPLOT MULTITHREADING HACK
# * ugly hack to fix pyplot multithreading issues
# * issue occurs when pyplot is called from a non-graphical adjsim instance
# * directly after being called from only a graphical adjsim instance
#-------------------------------------------------------------------------------
    @staticmethod
    def pyplotMultithreadingHack():
        pyplot.ion()
        pyplot.plot([1,2])
        pyplot.show()
        pyplot.close()
        pyplot.ioff()


# METHOD RESET ENVIRONMENT
#-------------------------------------------------------------------------------
    def clearEnvironment(self):
        del self.environment
        self.environment = Simulation.Environment()


# METHOD SIMULATE
#-------------------------------------------------------------------------------
    def simulate(self, length, graphicsEnabled=False, plotIndices=False,
            simulationType=Intelligence.SIMULATION_TYPE_TRAIN):

        # setup simulation globals
        Intelligence.SIMULATION_TYPE = simulationType

        # initalize simulation with/without graphics
        if graphicsEnabled:
            # perform threading initialization for graphics
            self.updateSemaphore = QtCore.QSemaphore(0)
            self.qApp = QtGui.QApplication([]) # no sys.argv provided
            self.view = Graphics.AdjGraphicsView(self.qApp.desktop().screenGeometry(), self.updateSemaphore)
            self.thread = Graphics.AdjThread(self.qApp, self.updateSemaphore, self.environment, length, plotIndices)

            self.thread.finished.connect(self.qApp.exit)
            self.qApp.connect(self.thread, self.thread.updateSignal, self.view.update)
            self.qApp.connect(self.thread, self.thread.plotSignal, self.view.plot)

            # begin simulation
            self.thread.start()
            self.qApp.exec_()

            # cleanup variables
            self.thread.quit()
            del self.thread
            del self.view
            del self.qApp
            del self.updateSemaphore

        else:
            # begin simulation
            self.environment.simulate(length, plotIndices=plotIndices)
