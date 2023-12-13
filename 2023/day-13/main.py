# read in input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()


def get_column(map, column):
    return "".join([row[column] for row in map])


def get_maps(input):
    # the names are lines of strings, each map split by an empty line
    maps = [[]]

    for line in input:
        if line == "":
            maps.append([])
        else:
            maps[-1].append(line)

    return maps


def check_if_mirror(map, index, dir="row"):
    if index == 0:
        return False

    if dir == "row":
        if index == len(map):
            return False

        closest_end = min(index, len(map) - index)
        for i in range(1, closest_end + 1):
            if map[index + i - 1] != map[index - i]:
                return False
        return True
    elif dir == "col":
        if index == len(map[0]):
            return False

        closest_end = min(index, len(map[0]) - index)
        for i in range(1, closest_end + 1):
            if get_column(map, index + i - 1) != get_column(map, index - i):
                return False
        return True


def get_reflection_line(map):
    for i in range(len(map) + 1):
        if check_if_mirror(map, i, "row"):
            return i, "row"
        
    for i in range(len(map[0]) + 1):
        if check_if_mirror(map, i, "col"):
            return i, "col"

    return None


def part1(input):
    maps = get_maps(input)

    total = 0

    for map in maps:
        num, direction = get_reflection_line(map)

        if direction == "row":
            total += num * 100
        else:
            total += num

    return total


def try_map_variants(map, original_reflection):
    # go through each row and column, and swap it to the opposite ("." or "#")
    for x in range(len(map)):
        for y in range(len(map[0])):
            new_map = map.copy()
            if map[x][y] == ".":
                new_map[x] = new_map[x][:y] + "#" + new_map[x][y + 1:]
            else:
                new_map[x] = new_map[x][:y] + "." + new_map[x][y + 1:]
            
            try:
                new_reflection, new_dir = get_reflection_line(new_map)

                if new_dir == "row" and original_reflection != new_reflection * 100:
                    return new_reflection * 100
                elif new_dir == "col" and original_reflection != new_reflection:
                    return new_reflection
            except:
                continue
    
    return original_reflection


def part2(input):
    maps = get_maps(input)

    total = 0

    for map in maps:
        original_reflection = 0
        num, direction = get_reflection_line(map)

        if direction == "row":
            original_reflection =  num * 100
        else:
            original_reflection = num
        
        new_reflection = try_map_variants(map, original_reflection)

        if new_reflection != original_reflection:
            original_reflection = new_reflection

        total += original_reflection
        
    return total


print("(Part 1) Summarized Notes: " + str(part1(input_raw)))
# I left my solution here so you can see what I did, but it doesn't work for some reason
print("NOT WORKING: (Part 2) Summarized Notes: " + str(part2(input_raw)))

#!/usr/bin/env python3

import sys

def transpose(grid):
	return list(map(''.join, zip(*grid)))

def count_differences(a, b):
	diff = 0
	for linea, lineb in zip(a, b):
		diff += sum(chara != charb for chara, charb in zip(linea, lineb))
		if diff > 1:
			break

	return diff

def find_reflections(grid):
	height = len(grid)
	perfect = imperfect = 0

	for size in range(1, height // 2 + 1):
		a = grid[:size]
		b = grid[size:2 * size][::-1]
		diff = count_differences(a, b)

		if diff == 0:
			perfect = size
		elif diff == 1:
			imperfect = size

		if perfect and imperfect:
			break

		a = grid[height - 2 * size:height - size]
		b = grid[height - size:][::-1]
		diff = count_differences(a, b)

		if diff == 0:
			perfect = height - size
		elif diff == 1:
			imperfect = height - size

		if perfect and imperfect:
			break

	return perfect, imperfect


# Open the first argument as input or use stdin if no arguments were given
fin = open("input.txt")

with fin:
	grids = fin.read().split('\n\n')

ans1 = ans2 = 0

for raw_grid in grids:
	g = raw_grid.splitlines()

	perfect, imperfect = find_reflections(g)
	ans1 += 100 * perfect
	ans2 += 100 * imperfect

	perfect, imperfect = find_reflections(transpose(g))
	ans1 += perfect
	ans2 += imperfect

print('(Copied - Part 2) Summarize with smudges: ', ans2)