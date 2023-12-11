# read input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()


def expand_universe(input):
    new_input = []
    for i in input:
        if i == "."*len(i):
            new_input.append("."*len(i))
            new_input.append("."*len(i))
        else:
            new_input.append(i)

    final_input = new_input.copy()

    columns_to_add = []
    # for columns that are all ["."] add another column of "." after it
    for i in range(len(new_input[0])):
        if "".join([new_input[j][i] for j in range(len(new_input))]) == "."*len(new_input):
            columns_to_add.append(i)

    index_add = 0
    for j in range(len(new_input)):
        for i in columns_to_add:
            # insert "." at index i+1
            final_input[j] = final_input[j][:i+1+index_add] + "." + final_input[j][i+1+index_add:]
            index_add += 1

            if i == columns_to_add[-1]:
                index_add = 0

    return final_input


def get_pairs(input):
    indexes = []
    # get all indexes of "#"
    for i in range(len(input)):
        for j in range(len(input[i])):
            if input[i][j] == "#":
                indexes.append([i, j])

    pairs = []

    for i, index in enumerate(indexes):
        for j in range(i, len(indexes)):
            if i != j:
                pairs.append([index, indexes[j]])
    
    return pairs


def get_shortest_path(pair):
    start = pair[0]
    end = pair[1]

    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def part1(input):
    # find rows and columns that are all ["."] then add another row of "." after it
    input = expand_universe(input)

    galaxy_pairs = get_pairs(input)

    shortest_paths = []

    for galaxy_pair in galaxy_pairs:
        shortest_paths.append(get_shortest_path(galaxy_pair))

    return sum(shortest_paths)


def get_empty_columns_and_rows(input):
    # return a list of 2 lists: empty rows and empty columns
    empty_rows = []
    empty_columns = []

    for i in range(len(input)):
        if input[i] == "."*len(input[i]):
            empty_rows.append(i)
    
    for i in range(len(input[0])):
        if "".join([input[j][i] for j in range(len(input))]) == "."*len(input):
            empty_columns.append(i)
    
    return (empty_columns, empty_rows)


def get_shortest_path_large(pair, empty_size, empty_columns, empty_rows):
    start = pair[0]
    end = pair[1]

    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])

    # get all rows and cols between start and end, and add empty_size if they are in empty_columns or empty_rows
    for i in range(min(start[0], end[0])+1, max(start[0], end[0])):
        if i in empty_rows:
            distance += empty_size - 1
    
    for i in range(min(start[1], end[1])+1, max(start[1], end[1])):
        if i in empty_columns:
            distance += empty_size - 1

    return distance


def part2(input):
    empty_cols, empty_rows = get_empty_columns_and_rows(input)

    # get distances again, but if it goes through an empty row or column, add 1000000 to the distance
    shortest_distances = []

    for pair in get_pairs(input):
        shortest_distances.append(get_shortest_path_large(pair, 1_000_000, empty_cols, empty_rows))
    
    return sum(shortest_distances)

# I feel really good about my optimizations and speeds for this one
print("(Part 1) Shortest Paths: " + str(part1(input_raw)))
print("(Part 2) Shortest Paths: " + str(part2(input_raw)))