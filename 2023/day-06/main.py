# read input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()

data = [list(filter(None, line.split(" ")))[1:] for line in input_raw]
data = [[int(num) for num in line] for line in data]

import math


def calculate_margins(times, bests):
    new_bests = [[] for _ in range(len(bests))]

    for i, time in enumerate(times):
        for j in range(time + 1):
            new_time = (time - j) * j
            if new_time > bests[i]:
                new_bests[i].append(new_time)

    return [len(bests) for bests in new_bests]


def part1(input):
    return math.prod(calculate_margins(data[0], data[1]))


def part2():
    new_data = [[int("".join([str(item) for item in line]))] for line in data]
    return math.prod(calculate_margins(new_data[0], new_data[1]))


# today's challenge was surprisingly easy
print("(Part 1) Multiplied margins of error: ", part1(data))
print("(Part 2) Multiplied margins of error: ", part2())
