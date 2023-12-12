# read in input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()


def parse_input(input):
    data = []

    for i in input:
        split = i.split(" ")
        data.append([split[0], [int(x) for x in split[1].split(",")]])

    return data


def check_is_valid(data, lengths):
    # get all groups of #s
    groups = []

    was_last_valid = False
    for i in range(len(data)):
        if data[i] == "#":
            if was_last_valid:
                groups[-1].append(i)
            else:
                groups.append([i])
            was_last_valid = True
        else:
            was_last_valid = False

    if lengths == [len(x) for x in groups]:
        return True
    else:
        return False


def wildcard_valid_count(data, lengths):
    # there are multiple wildcards (?), go through all possible combinations of replacing them with "#" or "."
    total = 0
    for char in ["#", "."]:
        if data.count("?") == 0:
            return 1
        # if the count of wildcards is 1
        elif data.count("?") == 1:
            # check if it is valid
            if check_is_valid(data.replace("?", char, 1), lengths):
                total += 1
        else:
            # if there are more than 1 wildcards, recurse
            total += wildcard_valid_count(data.replace("?", char, 1), lengths)

    return total


def part1(input):
    data = parse_input(input)

    counts = 0

    for i in data:
        counts += wildcard_valid_count(i[0], i[1])

    return counts


print("Be patient, this brute forces the answer, it will take a bit...")
print("(Part 1): Total Counts: " + str(part1(input_raw)))


# NOTE: not my code
import sys
from pathlib import Path
from functools import cache


def configuration_count(row: str, groups) -> int:
    def valid_group(start, length):
        valid = row[start : start + length].count(".") == 0
        valid = valid and len(row[start : start + length]) == length
        valid = valid and (start + length >= len(row) or row[start + length] in ".?")
        return valid

    @cache
    def recur(position, group_id):
        if group_id == len(groups):
            return row[position:].count("#") == 0
        if position >= len(row):
            return 0
        if row[position] == "#":
            if valid_group(position, groups[group_id]):
                return recur(position + groups[group_id] + 1, group_id + 1)
            else:
                return 0
        if valid_group(position, groups[group_id]):
            return recur(position + groups[group_id] + 1, group_id + 1) + recur(
                position + 1, group_id
            )
        return recur(position + 1, group_id)

    return recur(0, 0)


def parse_line(line):
    row, groups = line.split()
    groups = [int(c) for c in groups.split(",")]
    return row, groups


def unfold(record):
    row, groups = record
    return "?".join([row] * 5), groups * 5


def main():
    with open("input.txt") as f:
        records = list(map(parse_line, f.read().splitlines()))
        print(
            "(Copied - Part 2): "
            + str(sum(configuration_count(*unfold(record)) for record in records))
        )


if __name__ == "__main__":
    main()
