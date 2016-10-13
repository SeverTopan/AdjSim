#-------------------------------------------------------------------------------
# ADJECOSYSTEM SIMULATION FRAMEWORK
# Deisgned and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
from core import *
import sys

#-------------------------------------------------------------------------------
# MAIN EXECUTION SCRIPT
#-------------------------------------------------------------------------------
def main(args=sys.argv):
    """The main routine."""

    adjEcosystem = AdjEcosystem(args)
    adjEcosystem.generateTestClasses()
    adjEcosystem.environment.simulate(5)


# EXECUTIUON CALLBACK
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
