from collections import defaultdict, deque
from enum import Enum

print("Day 23 of Advent of Code!")

ELF = "#"


class Directions(Enum):
    N = (-1, 0)
    NW = (-1, -1)
    NE = (-1, 1)
    E = (0, 1)
    W = (0, -1)
    S = (1, 0)
    SW = (1, -1)
    SE = (1, 1)
    NIL = (0, 0)


SCANS = {
    (Directions.N, Directions.NE, Directions.NW): Directions.N,
    (Directions.S, Directions.SE, Directions.SW): Directions.S,
    (Directions.W, Directions.NW, Directions.SW): Directions.W,
    (Directions.E, Directions.NE, Directions.SE): Directions.E,
}

SCANNING_CYCLE = deque(SCANS.keys())


def get_elves(data):
    elves = set()
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == ELF:
                elves.add((i, j))
    return elves


def get_direction(elf, elves):
    i, j = elf
    potential_directions = []
    for scan in SCANNING_CYCLE:
        occupied = False
        for direction in scan:
            new_i, new_j = direction.value
            adjacent = (i + new_i, j + new_j)
            if adjacent in elves:
                occupied = True
                break
        if not occupied:
            potential_directions.append(SCANS[scan])

    new_direction = (
        potential_directions[0] if 0 < len(potential_directions) < 4 else Directions.NIL
    )

    return new_direction


def get_new_position(elf, elves, moves):
    i, j = elf
    direction = get_direction(elf, elves)
    new_i, new_j = direction.value
    moves[(i + new_i, j + new_j)].append(elf)


def get_all_moves(elves):
    moves = defaultdict(list)
    for elf in elves:
        get_new_position(elf, elves, moves)
    return moves


def move_elves(moves, elves):
    new_elves = set()
    for move in moves:
        if len(moves[move]) > 1:
            for position in moves[move]:
                new_elves.add(position)
        else:
            new_elves.add(move)
    no_more_moves = new_elves == elves
    return new_elves, no_more_moves


def box_elves(elves):
    all_i, all_j = [], []
    for i, j in elves:
        all_i.append(i)
        all_j.append(j)
    all_i.sort()
    all_j.sort()

    return (abs(all_i[0]) + abs(all_i[-1]) + 1) * (
        abs(all_j[0]) + abs(all_j[-1]) + 1
    ) - len(elves)


def spread_elves(elves):
    rounds_to_standstill = 0
    while True:
        moves = get_all_moves(elves)
        elves, no_more_moves = move_elves(moves, elves)
        SCANNING_CYCLE.rotate(-1)
        rounds_to_standstill += 1
        if rounds_to_standstill == 10:
            print("Empty tiles after 10 rounds:", box_elves(elves))
        if no_more_moves:
            print("Maximum rounds:", rounds_to_standstill)
            break


with open("map.txt", mode="r") as inp:
    print("Solution...")
    spread_elves(get_elves(inp.read().splitlines()))
