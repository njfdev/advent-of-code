# read input.txt
with open("input.txt", "r") as f:
    data = f.read().splitlines()


from tqdm import tqdm


mirror_redirection = {
    "/": [[[-1, 0], [0, -1]], [[1, 0], [0, 1]]],
    "\\": [[[1, 0], [0, -1]], [[-1, 0], [0, 1]]],
}


# beam is a tuple of ([y, x], [y, x]) where the first is the beam index and the second is the direction
def get_next_tiles(input, beam):
    try:
        new_index = [beam[0][0] + beam[1][0], beam[0][1] + beam[1][1]]

        # if next is ".", then return the index of that
        if input[new_index[0]][new_index[1]] == ".":
            return [new_index], [beam[1]]

        # if next is a "/" or "\", then return the next tile based on the mirror redirection
        elif (
            input[new_index[0]][new_index[1]] == "/"
            or input[new_index[0]][new_index[1]] == "\\"
        ):
            for redirection in mirror_redirection[input[new_index[0]][new_index[1]]]:
                if (
                    redirection[1][0] == -beam[1][0]
                    and redirection[1][1] == -beam[1][1]
                ):
                    return [new_index], [redirection[0]]
                elif (
                    redirection[0][0] == -beam[1][0]
                    and redirection[0][1] == -beam[1][1]
                ):
                    return [new_index], [redirection[1]]

        # if next is a "|"
        elif input[new_index[0]][new_index[1]] == "|":
            # if direction is vertical,
            if beam[1][1] == 0:
                return [new_index], [
                    beam[1],
                ]
            # if direction is horizontal, then return both vertical directions
            else:
                return [new_index, new_index], [
                    [1, 0],
                    [-1, 0],
                ]

        # if next is a "-"
        elif input[new_index[0]][new_index[1]] == "-":
            # if direction is horizontal,
            if beam[1][0] == 0:
                return [new_index], [
                    beam[1],
                ]
            # if direction is vertical, then return both horizontal directions
            else:
                return [new_index, new_index], [
                    [0, 1],
                    [0, -1],
                ]

        return None, None
    except IndexError:
        return None, None


def part1(input, starting_beam=[[0, -1], [0, 1]]):
    energized_tiles = []

    beams = [starting_beam]

    already_used_beams = []

    while len(beams) > 0:
        new_beams = []
        # print(beams)
        for beam in beams:
            next_tiles = get_next_tiles(input, beam)
            if next_tiles[0] is not None:
                for i, next_tile in enumerate(next_tiles[0]):
                    # if next_tile is not in input, then skip it
                    if (
                        next_tile[0] < 0
                        or next_tile[1] < 0
                        or next_tile[0] >= len(input)
                        or next_tile[1] >= len(input[0])
                    ):
                        continue
                    new_beam = [next_tile, next_tiles[1][i]]
                    if new_beam not in already_used_beams:
                        new_beams.append([new_beam[0], new_beam[1]])
                        if new_beam[0] not in energized_tiles:
                            energized_tiles.append(new_beam[0])
        already_used_beams.extend(new_beams)
        beams = new_beams

    return len(energized_tiles)


def part2(input):
    energized_tile_counts = []

    starting_beams = []

    for y in range(len(input)):
        starting_beams.append([[y, -1], [0, 1]])
        starting_beams.append([[y, len(input[0])], [0, -1]])

    for x in range(len(input[0])):
        starting_beams.append([[-1, x], [1, 0]])
        starting_beams.append([[len(input), x], [-1, 0]])

    for starting_beam in tqdm(starting_beams):
        energized_tile_counts.append(part1(input, starting_beam))

    return max(energized_tile_counts)


print("(Part 1) Energized Tiles: ", part1(data))
# this brute force approach works, but it takes a long time to run
print("(Part 2) Max Energized Tiles: ", part2(data))
