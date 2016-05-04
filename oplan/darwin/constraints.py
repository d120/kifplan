from .models import Constraint,AKConstraint


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


class AKWantsWeekdayConstraint(AKConstraint):
    """ checks that the AK is on one of the requested days of week """
    
    WEEKDAYS = {'mo':1,'di':2,'mi':3,'do':4,'fr':5,'sa':6,'so':7}
    
    def __init__(self, ak, weekdays):
        self.ak = ak
        self.weekdays = [ self.WEEKDAYS[wd[0:2]] for wd in weekdays.split('|') ]

    def check(self, genome):
        mismatches, messages = 0, []
        for ak, slot in genome.schedule:
            if ak == self.ak:
                if not slot.start.isoweekday() in self.weekdays:
                    mismatches += 1
                    messages.append("[weekday] AK {0} was not assigned to requested weekday.".format(ak))
                break
        
        return (mismatches, messages)



class AKBeforeDateTimeConstraint(AKConstraint):
    """ checks that the AK is on one of the requested days of week """
    
    def __init__(self, ak, check_dt):
        self.ak = ak
        self.check_dt = check_dt

    def check(self, genome):
        mismatches, messages = 0, []
        for ak, slot in genome.schedule:
            if ak == self.ak:
                if slot.start > self.check_dt:
                    mismatches += 1
                    messages.append("[AKBeforeDateTime] AK {0} was not assigned before requested date/time.".format(ak))
                break
        
        return (mismatches, messages)


class AKAfterDateTimeConstraint(AKConstraint):
    """ checks that the AK is on one of the requested days of week """
    
    def __init__(self, ak, check_dt):
        self.ak = ak
        self.check_dt = check_dt

    def check(self, genome):
        mismatches, messages = 0, []
        for ak, slot in genome.schedule:
            if ak == self.ak:
                if slot.start < self.check_dt:
                    mismatches += 1
                    messages.append("[AKAfterDateTime] AK {0} was assigned at {1}, before requested date/time {2}.".format(ak, slot.start, self.check_dt))
                break
        
        return (mismatches, messages)


""" constraints on the whole genome """
GLOBAL_CONSTRAINTS = [
    SlotsExclusivelyUsedConstraint(),
    EveryAKScheduledConstraint(),
]
