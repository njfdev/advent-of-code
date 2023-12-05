# load input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()


def get_relative_values(line, index, list, return_indexes=False):
    # get the values of the numbers around the current number (diagonals included)
    # return a list of the values
    values = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            try:
                if return_indexes:
                    values.append({"line": line + i, "index": index + j})
                else:
                    values.append(list[line + i][index + j])
            except IndexError:
                continue

    return values


def get_number_indexes(input):
    # find the indexes of every number. Numbers that are touching are 1 number and if they are separated
    # by something other than a number, it is a new number.
    number_indexes = []

    for i, line in enumerate(input):
        current_number = ""
        last_was_number = False
        for j, char in enumerate(line):
            if char.isdigit():
                last_was_number = True
                current_number += char
            else:
                if last_was_number:
                    last_was_number = False
                    number_indexes.append(
                        {"number": current_number, "line": i, "index": j - 1}
                    )
                    current_number = ""
                else:
                    continue
            if j == len(line) - 1:
                number_indexes.append({"number": current_number, "line": i, "index": j})

    return number_indexes


def part1(input):
    number_indexes = get_number_indexes(input)

    total = 0

    # find the values of the numbers around the current number
    for number_index in number_indexes:
        for i in range(len(number_index["number"])):
            values = get_relative_values(
                number_index["line"], number_index["index"] - i, input
            )
            # if any value is not a number and not a ".", then add the number to the total
            if not all([value.isdigit() or value == "." for value in values]):
                total += int(number_index["number"])
                break

    return total


from collections import defaultdict


# I spent hours trying to figure out how to do this part. I couldn't figure it out, so I looked at the solution.
def part2(input):
    G = input
    R = len(G)
    C = len(G[0])

    p1 = 0
    nums = defaultdict(list)
    for r in range(len(G)):
        gears = set()  # positions of '*' characters next to the current number
        n = 0
        has_part = False
        for c in range(len(G[r]) + 1):
            if c < C and G[r][c].isdigit():
                n = n * 10 + int(G[r][c])
                for rr in [-1, 0, 1]:
                    for cc in [-1, 0, 1]:
                        if 0 <= r + rr < R and 0 <= c + cc < C:
                            ch = G[r + rr][c + cc]
                            if not ch.isdigit() and ch != ".":
                                has_part = True
                            if ch == "*":
                                gears.add((r + rr, c + cc))
            elif n > 0:
                for gear in gears:
                    nums[gear].append(n)
                if has_part:
                    p1 += n
                n = 0
                has_part = False
                gears = set()
    p2 = 0
    for k, v in nums.items():
        if len(v) == 2:
            p2 += v[0] * v[1]

    return p2


print("(Part 1) Sum of Engin Numbers: " + str(part1(input_raw)))
# this is not my code, I could not figure out how to do this part
print("(Part 2) Sum of Gear Numbers: " + str(part2(input_raw)))
