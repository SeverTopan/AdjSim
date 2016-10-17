#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
from core import *
import tests
import sys

#-------------------------------------------------------------------------------
# MAIN EXECUTION SCRIPT
#-------------------------------------------------------------------------------
def main(args=sys.argv):
    """The main routine."""

    adjEcosystem = AdjEcosystem(args)
    tests.generateTestClasses_dogApple(adjEcosystem.environment)
    adjEcosystem.simulate(5)

    # get char press to exit
    input("Press Enter to Termainate")


# EXECUTIUON CALLBACK
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
