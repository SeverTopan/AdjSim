#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# * A Flexible framework on top of which to simulate the activity of an
# * 'ecosystem'.
# * Enivronment is set up via a configuration script at the beginning of each
# * simulation that sets cycle schedules, resource locations, etc.
#
# By Sever Topan
#-------------------------------------------------------------------------------
import sys

def horizontalRuler(length):
    msg = ""
    for i in range(length):
        msg += "-"

    return msg

#-------------------------------------------------------------------------------
# CLASS ADJECOSYSTEM
#-------------------------------------------------------------------------------
class AdjEcosystem:
    """docstring for AdjEcosystem."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self, argv):
        self.printWelcome()
        self.parseConfigFile(argv)

# METHOD PRINT WELCOME
#-------------------------------------------------------------------------------
    @staticmethod
    def printWelcome():
        welcomeMessage = "- AdjEcosystem -"

        print horizontalRuler(len(welcomeMessage))
        print welcomeMessage
        print horizontalRuler(len(welcomeMessage))

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



#-------------------------------------------------------------------------------
# MAIN EXECUTION SCRIPT
#-------------------------------------------------------------------------------
adjEcosystem = AdjEcosystem(sys.argv)
