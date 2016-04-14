#!/usr/bin/env python3

import sys, os, argparse

from src.serialization import *
from src.evolution import find_solution


def main():
    """
    runs the algorithm, schedules all AKs in the best possible way

    Usage:
        --slots         path to slots JSON file
        --aks           path to AKs JSON file
        --iterations    number of generations to run
        --fertility     number of mutations to create per generation
    """

    # argument parsing
    parser = argparse.ArgumentParser(description='KIF AK scheduling tool')
    parser.add_argument('--slots', help='path to slots JSON file')
    parser.add_argument('--aks', help='path to AKs JSON file')
    parser.add_argument('--iterations', help='number of generations to run', default=100)
    parser.add_argument('--fertility', help='number of mutations to create per generation', default=4)
    args = parser.parse_args()

    # check argument validity
    if args.slots is None or not os.path.exists(args.slots):
        print("please provide a slots file")
        sys.exit(1)
    if args.aks is None or not os.path.exists(args.aks):
        print("please provide a aks file")
        sys.exit(1)

    # load data
    with open(args.slots) as f:
        slots = slotsFromJSON(f.read())
    with open(args.aks) as f:
        aks = aksFromJSON(f.read())

    # calculate solution
    solution, fitness, messages = find_solution(slots, aks, int(args.iterations), int(args.fertility))

    # print out result
    if len(messages) > 0:
        print("\nSome problems exist with this solution:")
        for message in messages:
            print(message)
    print()
    print(solution)


if __name__ == '__main__':
    main()
