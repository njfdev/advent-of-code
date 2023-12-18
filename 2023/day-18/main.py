# read input.txt
with open("input.txt", "r") as f:
    data = f.read().strip().splitlines()


def run_step(y, x, direction, map):
    coordinate = y,x

    if direction == "U":
        coordinate = y - 1, x
    elif direction == "D":
        coordinate = y + 1, x
    elif direction == "L":
        coordinate = y, x - 1
    elif direction == "R":
        coordinate = y, x + 1
    
    # if the coordinate is outside the map, expand the row/col with "."
    if coordinate[0] < 0:
        map.insert(0, ["." for _ in range(len(map[0]))])
        coordinate = 0, coordinate[1]
    elif coordinate[0] >= len(map):
        map.append(["." for _ in range(len(map[0]))])
    elif coordinate[1] < 0:
        for row in map:
            row.insert(0, ".")
        coordinate = coordinate[0], 0
    elif coordinate[1] >= len(map[0]):
        for row in map:
            row.append(".")
    
    # now make the coordinate in the direction a "#"
    map[coordinate[0]][coordinate[1]] = "#"

    return map, coordinate[0], coordinate[1]


def run_instruction(y, x, instruction, map):
    new_map = map.copy()
    for _ in range(int(instruction[1])):
        new_map, y, x = run_step(y, x, instruction[0], new_map)
    return new_map, y, x


def get_touching(y, x, map):
    visited = set()
    stack = [(y, x)]

    while stack:
        y, x = stack.pop()
        visited.add((y, x))

        surrounding = [
            (y - 1, x),
            (y + 1, x),
            (y, x - 1),
            (y, x + 1),
            (y - 1, x - 1),
            (y - 1, x + 1),
            (y + 1, x - 1),
            (y + 1, x + 1)
        ]

        for coordinate in surrounding:
            if coordinate[0] < 0 or coordinate[0] >= len(map) or coordinate[1] < 0 or coordinate[1] >= len(map[0]):
                continue
            elif map[coordinate[0]][coordinate[1]] == "#":
                continue
            elif map[coordinate[0]][coordinate[1]] == "." and coordinate not in visited:
                stack.append(coordinate)

    return list(visited)

def part1(input):
    instructions = [instruction.split(" ")[:2] for instruction in input]

    map = [["."]]
    y, x = 0, 0

    for instruction in instructions:
        map, y, x = run_instruction(y, x, instruction, map)
    
    # now we have an outline made of "#", so now we need to fill it in with "#"
    new_map = map.copy()

    # get all coords at the edge of the map that is a "."
    edge_coords = []
    for y, row in enumerate(map):
        if new_map[y][0] == ".":
            edge_coords.append((y, 0))
        if new_map[y][-1] == ".":
            edge_coords.append((y, len(row) - 1))
    for x, col in enumerate(map[0]):
        if new_map[0][x] == ".":
            edge_coords.append((0, x))
        if new_map[-1][x] == ".":
            edge_coords.append((len(map) - 1, x))
    
    # now we have all the edge coords, we need to get all the coords that are touching the edge coords
    for coord in edge_coords:
        touching = get_touching(coord[0], coord[1], new_map)
        for coord in touching:
            new_map[coord[0]][coord[1]] = "x"
    
    # replace all "." with "#"
    for y, row in enumerate(new_map):
        for x, col in enumerate(row):
            if col == ".":
                new_map[y][x] = "#"

    # return the number of "#" in the map
    return sum([row.count("#") for row in new_map])


print("(Part 1) Cubic meters of lava: ", part1(data))


# NOTE: Not my code
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

with open("input.txt") as f:
    lines = f.read().splitlines()

points = [(0, 0)]
boundary = 0

for line in lines:
    *_, color = line.split()
    instructions = color[2:-1]
    dr, dc = DIRECTIONS[int(instructions[-1])]
    steps = int(instructions[:-1], 16)
    boundary += steps
    row, column = points[-1]
    points.append((row + dr * steps, column + dc * steps))

print(
    "(Copied - Part 2) Cubic meters of lava: ", 
    abs(
        sum(
            x1 * y2 - x2 * y1
            for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1])
        )
    )
    // 2
    + boundary // 2
    + 1
)