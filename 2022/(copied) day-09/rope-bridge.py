#!/usr/bin/env python3

file = open("ropes.txt")
loi = file.readlines()

loi = list(map(lambda x: (x.split(" ")[0], int(x.split(" ")[1])), loi))

file.close()


def dir_to_num(d):
    if d == "R":
        return (1, 0)
    elif d == "L":
        return (-1, 0)
    elif d == "U":
        return (0, 1)
    elif d == "D":
        return (0, -1)


# Moves the tail and returns the change that took place for the current tail (to be used on the next tail adjustment)
def move_tail(head_coords, tail_coords, change):

    former_location = (tail_coords[0], tail_coords[1])

    if (
        abs(tail_coords[0] - head_coords[0]) > 1
        or abs(tail_coords[1] - head_coords[1]) > 1
    ):
        if change[0] != 0 and change[1] != 0:
            if tail_coords[0] == head_coords[0]:
                tail_coords[1] += change[1]
            elif tail_coords[1] == head_coords[1]:
                tail_coords[0] += change[0]
            else:
                tail_coords[0] += change[0]
                tail_coords[1] += change[1]
        else:

            tail_coords[0] += change[0]
            tail_coords[1] += change[1]

            if change[0] != 0 and tail_coords[1] != head_coords[1]:
                tail_coords[1] = head_coords[1]
            elif change[1] != 0 and tail_coords[0] != head_coords[0]:
                tail_coords[0] = head_coords[0]

    return (tail_coords[0] - former_location[0], tail_coords[1] - former_location[1])


def Solution(inpt, num_of_ropes):

    coords = set()

    rope_coords = [[0, 0] for i in range(num_of_ropes)]

    coords.add(tuple(rope_coords[-1]))

    for instr in inpt:
        dir_ = instr[0]
        for i in range(instr[1]):
            change = dir_to_num(dir_)

            rope_coords[0][0] += change[0]
            rope_coords[0][1] += change[1]

            # We start at 1 so that we don't move the head twice
            for j in range(1, num_of_ropes):
                change = move_tail(rope_coords[j - 1], rope_coords[j], change)

                # No need to keep going once we reach a point of no movement
                if change == (0, 0):
                    break

            coords.add(tuple(rope_coords[-1]))

    return len(coords)


print(Solution(loi, 2))
print(Solution(loi, 10))
