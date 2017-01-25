#-------------------------------------------------------------------------------
# ADJSIM SIMULATION FRAMEWORK
# Designed and developed by Sever Topan
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# CLASS TARGET PREDICATE
#-------------------------------------------------------------------------------
class TargetPredicate(object):
    """docstring for TargetPredicate."""

    ENVIRONMENT = -1
    SOURCE = -2

    def __init__(self, target, predicate):
        super(TargetPredicate, self).__init__()
        self.target = target
        self.predicate = predicate

#-------------------------------------------------------------------------------
# CLASS TARGET SET
#-------------------------------------------------------------------------------
class TargetSet(object):
    """docstring for TargetSet."""
    def __init__(self, environment, source, targets = None):
        super(TargetSet, self).__init__()
        self.environment = environment
        self.source = source
        if targets == None:
            targets = []
        self.targets = targets


#-------------------------------------------------------------------------------
# CLASS HISTORY
#-------------------------------------------------------------------------------
class HistoricTimestep(object):
    """docstring for HistoricTimestep."""

# METHOD __INIT__
#-------------------------------------------------------------------------------
    def __init__(self):
        super(HistoricTimestep, self).__init__()
        self.abilityCast = None
        self.thoughtMutableTraitValues = None
        self.perceptionTuple = None
        self.goalEvaluationAchieved = 0
        self.moveScore = 0
