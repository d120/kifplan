from .models import Constraint


# global constraints (these work on the genome itself)

class SlotsExclusivelyUsedConstraint(Constraint):
    """ counts slot collisions """

    def check(self, genome):
        mismatches, messages = 0, []
        for ak, slot in genome.schedule:
            for ak2, slot2 in genome.schedule:
                if slot is not None and slot2 is not None and ak != ak2 and slot == slot2:
                    mismatches += 1
                    messages.append("[slot collision] AKs {0} and {1} are both assigned to slot {2}".format(ak, ak2, slot))
        return (mismatches, messages)


class EveryAKScheduledConstraint(Constraint):
    """ counts AKs that have not been scheduled """

    def check(self, genome):
        mismatches, messages = 0, []
        for ak, slot in genome.schedule:
            if (slot is None):
                mismatches += 1
                messages.append("[not scheduled] AK {0} was not assigned to a slot.".format(ak))
        return (mismatches, messages)


""" constraints on the whole genome """
GLOBAL_CONSTRAINTS = [
    SlotsExclusivelyUsedConstraint(),
    EveryAKScheduledConstraint(),
]
