import sys
from time import perf_counter as pc

from .genetics import inception, fitness, mutate


def find_solution(slots, aks, iterations, fertility, mutations):
    """
    runs the evolutionary algorithm and returns a hopefully good solution
    """

    t0 = pc()
    genome = inception(slots, aks)
    score, messages = fitness(genome)

    print("Inception: created first generation genome. Fitness: {0}".format(score))
    print("Starting evolution for {0} iterations with {1} mutations per generation...".format(iterations, fertility))

    for generation in range(iterations):
        # if perfect fitness has been reached, stop computing
        if score == 1:
            print("  Generation: {0}  Reached fitness of 1 which can not be increased.".format(generation))
            break
        # generate mutated children genomes
        candidates = [mutate(genome, mutations) for i in range(fertility)]
        # find best mutation
        for candidate in candidates:
            if fitness(candidate)[0] > score:
                print("reassign")
                # use fittest for next generation
                genome = candidate
                score, messages = fitness(genome)
        print("  Generation: {0}  Fitness: {1}".format(generation, score)),

    print("Done in {0} seconds. Found solution with fitness {1}".format(round(pc()-t0, 4), round(score, 6)))
    return (genome, score, messages)
