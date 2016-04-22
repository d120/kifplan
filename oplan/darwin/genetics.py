import random

from .constraints import GLOBAL_CONSTRAINTS
from .models import *


def fitness(genome):
    """
    calculates a "single big number" (fitness) for a given genome, to allow
    comparison

    Currently returns reciprocal of number of failed constraints. Fails are counted
    from 1 to prevent division by 0, and to have 1 (100%) being the best possible
    fitness.

    genome (Genome): solution to measure fitness for
    """

    errors = 1
    all_messages = []

    for ak, slot in genome.schedule:
        if ak == None: continue
        for constraint in ak.constraints:
            mismatches, messages = constraint.check(genome)
            errors += mismatches
            all_messages.extend(messages)

    for constraint in GLOBAL_CONSTRAINTS:
        mismatches, messages = constraint.check(genome)
        errors += mismatches
        all_messages.extend(messages)

    return (1 / errors, all_messages)


def mutate(genome, mutation_count):
    """
    generates a mutation of the given genome by swapping slot mappings
    """

    genome = Genome.copy(genome)
    for i in range(mutation_count):
        swapA, swapB = [random.randint(0, len(genome.schedule) - 1) for i in range(2)]

        tmp = genome.schedule[swapA][1]
        genome.schedule[swapA] = (genome.schedule[swapA][0], genome.schedule[swapB][1])
        genome.schedule[swapB] = (genome.schedule[swapB][0], tmp)

    return genome


def inception(slots, aks):
    """
    generates the first generation genome naively
    """

    mapping = []
    used_slots = []

    for ak in aks:
        selected_slot = None
        for slot in slots:
            if slot not in used_slots:
                selected_slot = slot
                used_slots.append(slot)
                break
        mapping.append((ak, selected_slot))
    
    for slot in slots:
        if slot not in used_slots:
            mapping.append((None, slot))
            used_slots.append(slot)
            break
            
    return Genome(mapping)
