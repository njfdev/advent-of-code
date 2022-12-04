def fully_contains(range1, range2):
    # Check if range1 fully contains range2
    start1, end1 = map(int, range1.split("-"))
    start2, end2 = map(int, range2.split("-"))
    return start1 <= start2 and end1 >= end2


def find_fully_contained_pairs(pairs):
    # Find the number of pairs where one range fully contains the other
    count = 0
    for pair in pairs:
        range1, range2 = pair.split(",")
        if fully_contains(range1, range2) or fully_contains(range2, range1):
            count += 1
    return count


# Read the pairs from the input file
with open("pairs.txt", "r") as f:
    pairs = f.readlines()

# Strip the newline characters from the pairs
pairs = [pair.strip() for pair in pairs]

# Print the number of fully contained pairs
print(find_fully_contained_pairs(pairs))
