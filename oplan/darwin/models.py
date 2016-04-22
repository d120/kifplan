import time
from oplan.darwin import config


class Slot:
    """
    represents a time slot that can be scheduled an AK

    If there is more than one room available at a given time, several Slot
    objects must be created as a Slot object can only correspond to one AK
    instance at most.

    start (struct_time): start time of this slot, end time is implied by slot length
    room (string): room for this slot
    """

    def __init__(self, start, room):
        self.start = start
        self.room = room

    def __repr__(self):
        return "{0} {1}".format(self.start.strftime(config.DATETIME_FORMAT), self.room)

    def __eq__(self, other):
        return self.start == other.start and self.room == other.room


class AK:
    """
    represents a single AK, as announced in the wiki

    name (string): AK title
    length (integer): duration in slot lengths
    host (Kiffel): person to present and lead this AK
    constraints (List of AKConstraint): constraints for this AK
    """

    def __init__(self, name, host, length, constraints=None):
        if constraints == None: constraints = []
        self.name = name
        self.host = host
        self.length = length
        self.constraints = constraints

    def __repr__(self):
        return "{0} ({1})".format(self.name, self.host)

    def __eq__(self, other):
        return self.name == other.name and self.host == other.host and self.length == other.length


class Genome:
    """
    represents a single solution to the scheduling problem

    This is a single step in the genetic algorithm. Its quality can be measured,
    and it can be transmuted.

    schedule (List of AK-Slot-Tuples): proposed solution as key-value-mapping
    """

    def __init__(self, schedule):
        self.schedule = schedule

    def __repr__(self):
        return str(self.schedule)

    def copy(other):
        return Genome(other.schedule[:])


class Constraint:
    """
    represents a constraint that can be checked against a genome

    This is an abstract base class, concrete implementations reside in constraints.py

    genome (Genome): current solution to test constraints against
    """

    def check(genome):
        raise NotImplementedError("check() on Constraint not implemented in subclass")


class AKConstraint(Constraint):
    """
    represents a constraint on an AK that can be checked against a genome

    This is an abstract base class, concrete implementations reside in constraints.py

    ak (AK): AK instance this Contraint is bound to
    """

    def __init__(self, ak):
        self.ak = ak
