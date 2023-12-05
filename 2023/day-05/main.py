# load input.txt
with open("input.txt", "r") as f:
    data = f.read().splitlines()

import itertools
from tqdm import tqdm


def get_seeds(input):
    seeds = input[0].split(": ")[1].split(" ")
    seeds = list(filter(None, seeds))
    return seeds


def get_mappings(input):
    mappings = []
    # split input into groups by empty lines
    map_groups = [
        list(g) for k, g in itertools.groupby(input, lambda x: x == "") if not k
    ]
    for i, group in enumerate(map_groups):
        for k, line in enumerate(group):
            if k == 0:
                mappings.append([])
                continue
            mappings[i].append(line.split(" "))

    # remove mappings that don't have any entries
    mappings = list(filter(None, mappings))

    return mappings


from functools import cache

mappings = get_mappings(data.copy())


def convert_seed(seed, mapping):
    # find if seed is in mapping
    if int(seed) >= int(mapping[1]) and int(seed) <= int(mapping[1]) + int(mapping[2]):
        return int(mapping[0]) + (int(seed) - int(mapping[1]))
    return None


def part1(seeds):
    final_locations = []

    for seed in seeds:
        for mapping in mappings:
            new_seed = None
            for map_portion in mapping:
                new_seed = convert_seed(seed, map_portion)
                if new_seed != None:
                    break
            if new_seed == None:
                new_seed = seed
            seed = new_seed

        final_locations.append(int(new_seed))

    return min(final_locations)


def get_overlap(seed_range, mapping_range):
    if (
        seed_range[0] >= mapping_range[1]
        and seed_range[1] <= mapping_range[1] + mapping_range[2]
    ):
        overlap = [None, None]
        overlap_end = (mapping_range[1] + mapping_range[2]) - seed_range[0]
        if overlap_end < 0:
            overlap_end = 0
        overlap[0] = mapping_range[1] + mapping_range[2] - overlap_end
        overlap[1] = max(seed_range[1], mapping_range[1])

        return overlap
    return None


def remove_overlap(seed_range, mapping_range):
    new_ranges = []
    if (
        seed_range[0] < mapping_range[1] + mapping_range[2]
        and seed_range[1] > mapping_range[1]
    ):
        new_ranges.append([seed_range[1], mapping_range[1]])
        new_ranges.append([mapping_range[1] + mapping_range[2], seed_range[0]])
    elif seed_range[0] <= mapping_range[1]:
        new_ranges.append([seed_range[1], mapping_range[1]])
    elif seed_range[1] >= mapping_range[1] + mapping_range[2]:
        new_ranges.append([mapping_range[1] + mapping_range[2], seed_range[0]])
    if len(new_ranges) == 0:
        return [mapping_range[1], mapping_range[1] + mapping_range[2]]
    return new_ranges


seeds = get_seeds(data)

print("(Part 1) Lowest Location: ", part1(seeds))
from functools import reduce

seed, *mappings = open("input.txt").read().split("\n\n")
seeds = list(map(int, seed.split()[1:]))


def lookup(inputs, mapping):
    for start, length in inputs:
        while length > 0:
            for m in mapping.split("\n")[1:]:
                dst, src, len = map(int, m.split())
                if src <= start < src + len:
                    len -= max(start - src, len - length)
                    yield (start - src + dst, len)
                    start += len
                    length -= len
                    break
            else:
                yield (start, length)
                break


# I could not figure out how to do this part
print(
    "(Part 1 Copied Code): Lowest Location: "
    + str(min(reduce(lookup, mappings, zip(seeds[0::2], seeds[1::2])))[0])
)
