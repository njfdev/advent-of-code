# read input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()


def parse_input(input):
    directions = input[0]

    navigation_map = {}

    for navigation in input[2:]:
        nav_parsed = navigation.split(" = ")
        left_right_map = nav_parsed[1][1:len(nav_parsed[1]) - 1].split(", ")
        navigation_map[nav_parsed[0]] = [left_right_map[0], left_right_map[1]]
    
    return directions, navigation_map


def part1(input):
    directions, navigation_map = parse_input(input)
    
    total_steps = 0

    last_navigation = navigation_map["AAA"]
    last_navigation_step = "AAA"
    last_direction_index = 0

    while True:
        direction_int = 0
        if directions[last_direction_index] == "R":
            direction_int = 1
        last_navigation_step = last_navigation[direction_int]
        last_navigation = navigation_map[last_navigation[direction_int]]
        last_direction_index += 1
        if last_direction_index >= len(directions):
            last_direction_index = 0
        total_steps += 1
        if last_navigation_step == "ZZZ":
            break

    return total_steps


from functools import cache


def part2(input):
    directions, navigation_map = parse_input(input)
    
    total_steps = 0

    last_navigation = []

    for _, (k, v) in enumerate(navigation_map.items()):
        if k.endswith("A"):
            last_navigation.append({ "key": k, "nav": v })

    last_navigation = last_navigation[:1]

    last_direction_index = 0

    @cache
    def get_next(nav1, nav2):
        direction_int = 0
        if directions[last_direction_index] == "R":
            direction_int = 1
        nav = [nav1, nav2][direction_int]
        return { "key": nav, "nav": navigation_map[nav] }

    while True:
        for i, ghost in enumerate(last_navigation):
            last_navigation[i] = get_next(ghost["nav"][0], ghost["nav"][1])
        last_direction_index += 1
        if last_direction_index >= len(directions):
            last_direction_index = 0
        total_steps += 1

        # if all ghosts key end with Z, break
        if all(ghost["key"].endswith("Z") for ghost in last_navigation):
            break

    return total_steps


print("(Part 1) Total steps: ", part1(input_raw))
# This is very slow, and I am not sure how to optimize it, so I never got the answer
#print("(Part 2) Total steps: ", part2(input_raw))

import math
from itertools import cycle

with open("input.txt") as f:
    lines = f.read().splitlines()

steps, _, *nodes = lines
instructions = cycle(steps)

tree = {}
for node in nodes:
    parent, children = node.split(" = ")
    left, right = children[1:-1].split(", ")
    tree[parent] = (left, right)

current_nodes = [node for node in tree if node.endswith("A")]
steps = []
for node in current_nodes:
    required_steps = 0
    current_node = node
    while True:
        required_steps += 1

        instruction = 0 if next(instructions) == "L" else 1
        current = tree[current_node][instruction]

        if current.endswith("Z"):
            break

        current_node = current

    steps.append(required_steps)

# this is not my code
print("(Not my code - Part 2): Total Steps: " + str(math.lcm(*steps)))