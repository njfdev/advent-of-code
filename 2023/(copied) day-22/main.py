# read input.txt
input_raw = open("input.txt", "r").read().strip().splitlines()


class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        # start and end are (x, y, z) coords with z as height
        # get which direction is different from start to end
        direction = 0
        for i in range(3):
            if start[i] != end[i]:
                direction = i
                break
        
        # add blocks that belong to this brick
        self.blocks = []
        for i in range(start[direction], end[direction]+1):
            # add block to list
            block = list(start)
            block[direction] = i
            self.blocks.append(tuple(block))

    def __repr__(self):
        return f"Brick({self.start}, {self.end})"
    
    def get_blocks(self):
        return self.blocks
    
    def move_down(self, distance):
        # move all blocks down by distance
        new_blocks = []
        for block in self.blocks:
            new_blocks.append((block[0], block[1], block[2] - distance))
        self.blocks = new_blocks
        # update start and end
        self.start = (self.start[0], self.start[1], self.start[2] - distance)
        self.end = (self.end[0], self.end[1], self.end[2] - distance)

    def get_lowest_block_z(self):
        lowest = 0
        for block in self.blocks:
            if block[2] > lowest:
                lowest = block[2]
        return lowest


def get_beneath_block(block, bricks):
    if block[2] == 1:
        return []
    # go through all get_blocks() of all bricks and find where x and y are the same
    # and z is less than the current block
    blocks = []
    for brick in bricks:
        for b in brick.get_blocks():
            if b[0] == block[0] and b[1] == block[1] and b[2] < block[2]:
                blocks.append(b)
    return blocks


def get_beneath_brick(brick, bricks):
    blocks = []
    for b in brick.get_blocks():
        beneath_block = get_beneath_block(b, bricks)
        for bl in beneath_block:
            if bl not in blocks and bl not in brick.get_blocks():
                blocks.append(bl)
    return blocks


def get_bricks_beneath_brick(brick, bricks):
    new_bricks = []
    for b in bricks:
        if b is brick:
            continue
        for block in b.get_blocks():
            for bl in brick.get_blocks():
                if (bl[0] == block[0] and bl[1] == block[1] and bl[2] - 1 == block[2]):
                    new_bricks.append(b)
                    break

    return new_bricks


def get_brick_falling_distance(brick, bricks):
    # get all blocks beneath this brick
    blocks = get_beneath_brick(brick, bricks)
    # get highest block
    highest = 1
    for block in blocks:
        if block[2] > highest:
            highest = block[2]
    # return distance
    return brick.start[2] - highest - 1


def can_disintegrate_brick(brick, bricks):
    # get all the bricks above this brick
    bricks_supported = []
    for b in bricks:
        # if brick already in bricks_supported, skip
        if b in bricks_supported or b == brick:
            continue
        for block in b.get_blocks():
            # if brick already in bricks_supported, skip
            if b in bricks_supported:
                continue
            for bl in brick.get_blocks():
                if bl[0] == block[0] and bl[1] == block[1] and bl[2] + 1 == block[2]:
                    bricks_supported.append(b)
                    break
                    
    # if all bricks above this brick have 2 or more blocks supported, return True
    for b in bricks_supported:
        bricks_beneath = get_bricks_beneath_brick(b, bricks)
        # if brick is in bricks_beneath, remove it
        if brick in bricks_beneath:
            bricks_beneath.remove(brick)
        if len(bricks_beneath) < 1:
            return False
    return True


def part1(input):
    bricks = []
    for line in input:
        start, end = line.split("~")
        start = tuple(map(int, start.split(",")))
        end = tuple(map(int, end.split(",")))
        bricks.append(Brick(start, end))

    has_brick_fallen = False
    while not has_brick_fallen:
        has_brick_fallen = False
        # sort bricks by the lowest z value
        bricks.sort(key=lambda brick: brick.get_lowest_block_z())
        for brick in bricks:
            # get distance to fall
            distance = get_brick_falling_distance(brick, bricks)
            if distance > 0:
                # move brick down
                brick.move_down(distance)
                # check if any bricks have fallen
                has_brick_fallen = True

    #print(bricks)

    # get all bricks that can be disintegrated
    disintegrated_brick_count = 0
    for brick in bricks:
        if can_disintegrate_brick(brick, bricks):
            disintegrated_brick_count += 1

    return disintegrated_brick_count


print("(My failed attempt - Part 1) Number of safely disintegrated bricks:", part1(input_raw))

# not my code
from collections import defaultdict

def ints(line):
    return tuple(map(int, line.replace('~',',').split(',')))

def dropped_brick(tallest, brick):
    peak = max(tallest[(x, y)] for x in range(brick[0], brick[3] + 1) for y in range(brick[1], brick[4] + 1))
    dz = max(brick[2] - peak - 1, 0)
    return (brick[0], brick[1], brick[2] - dz, brick[3], brick[4], brick[5] - dz)

def drop(tower):
    tallest = defaultdict(int)
    new_tower = []
    falls = 0
    for brick in tower:
        new_brick = dropped_brick(tallest, brick)
        if new_brick[2] != brick[2]:
            falls += 1
        new_tower.append(new_brick)
        for x in range(brick[0], brick[3] + 1):
            for y in range(brick[1], brick[4] + 1):
                tallest[(x, y)] = new_brick[5]
    return falls, new_tower

def solve(data):
    bricks = sorted([ints(line) for line in data], key=lambda brick: brick[2])
    _, fallen = drop(bricks)
    p1 = p2 = 0
    for i in range(len(fallen)):
        removed = fallen[:i] + fallen[i + 1:]
        falls, _ = drop(removed)
        if not falls:
            p1 += 1
        else:
            p2 += falls
    return p1, p2

p1, p2 = solve(input_raw)
print("(Copied - Part 1) Number of safely disintegrated bricks:", p1)
print("(Copied - Part 2) Sum of # of other bricks that would fall:", p2)