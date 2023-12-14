# read in input.txt
with open("input.txt", "r") as f:
    input = f.read().splitlines()

def get_offset(x, y, direction):
    if direction == "up":
        return y - 1
    elif direction == "down":
        return y + 1
    elif direction == "right":
        return x + 1
    elif direction == "left":
        return x - 1

def move_bolder_towards(map, by, bx, direction="up"):
    map = map.copy()

    if map[by][bx] != "O":
        print("Invalid bolder error")
        return map
    
    new_x = bx
    new_y = by

    if direction == "up":
        new_y -= 1
    elif direction == "down":
        new_y += 1
    elif direction == "right":
        new_x += 1
    elif direction == "left":
        new_x -= 1
    
    if new_x >= len(map[0]) or new_y >= len(map):
        return map
    
    if new_x < 0 or new_y < 0:
        return map
    elif direction == "down" and new_y >= len(map):
        return map
    elif direction == "right" and new_x >= len(map[0]):
        return map

    while map[new_y][new_x] == ".":
      if direction == "up" or direction == "down":
          new_y = get_offset(new_x, new_y, direction)
      elif direction == "right" or direction == "left":
          new_x = get_offset(new_x, new_y, direction)

      if new_x < 0 or new_y < 0:
          break
      elif direction == "down" and new_y >= len(map):
          break
      elif direction == "right" and new_x >= len(map[0]):
          break

    if direction == "up":
        new_y += 1
    elif direction == "down":
        new_y -= 1
    elif direction == "right":
        new_x -= 1
    elif direction == "left":
        new_x += 1

    map[by] = map[by][:bx] + "." + map[by][bx + 1:]
    map[new_y] = map[new_y][:new_x] + "O" + map[new_y][new_x + 1:]
    
    return map

from functools import cache

@cache
def tilt_platform(map, direction="up"):
    new_map = map.splitlines().copy()

    # get every index that is "O"
    bolder_indexes = []
    for y in range(len(new_map)):
        for x in range(len(new_map[y])):
            if new_map[y][x] == "O":
                bolder_indexes.append((y, x))
    
    # sort based off of direction, e.g. if up sort by y ascending then x ascending
    if direction == "up":
        bolder_indexes.sort(key=lambda x: (x[0], x[1]))
    elif direction == "down":
        bolder_indexes.sort(key=lambda x: (x[0], x[1]), reverse=True)
    # if left, sort by y ascending then x ascending
    elif direction == "left":
        bolder_indexes.sort(key=lambda x: (x[1], x[0]))
    # if right, sort by y ascending then x descending
    elif direction == "right":
        bolder_indexes.sort(key=lambda x: (x[1], x[0]), reverse=True)

    for by, bx in bolder_indexes:
        new_map = move_bolder_towards(new_map, by, bx, direction)
    
    return new_map


def part1(input):
    
    new_map = tilt_platform("\n".join(input), "up")

    total_score = 0

    for i in range(len(new_map)):
        for j in range(len(new_map[i])):
            if new_map[i][j] == "O":
                total_score += len(new_map) - i

    return total_score

@cache
def run_cycle(map):
    new_cycle_part = map.splitlines()

    new_cycle_part = tilt_platform("\n".join(new_cycle_part), "up")
    new_cycle_part = tilt_platform("\n".join(new_cycle_part), "left")
    new_cycle_part = tilt_platform("\n".join(new_cycle_part), "down")
    new_cycle_part = tilt_platform("\n".join(new_cycle_part), "right")

    return new_cycle_part

@cache
def run_cycle_iter(map_data, amount=10):
    for i in range(amount):
        map_data = "\n".join(run_cycle(map_data))
    
    return map_data.splitlines()

from tqdm import tqdm

def part2(input):
    final_map = input.copy()

    for i in tqdm(range(10000000)):
        final_map = run_cycle_iter("\n".join(final_map), 100)
        
    total_score = 0

    for i in range(len(final_map)):
        for j in range(len(final_map[i])):
            if final_map[i][j] == "O":
                total_score += len(final_map) - i

    return total_score

print("(Part 1) Total Load: " + str(part1(input)))
print("(Part 2) Total Load after Cycles: " + str(part2(input)))