def find_overlapping_pairs(pairs):
    # Find the number of pairs that overlap
    count = 0
    for pair in pairs:
        range1, range2 = pair.split(",")
        start1, end1 = map(int, range1.split("-"))
        start2, end2 = map(int, range2.split("-"))
        # Check if the ranges overlap
        if (start1 >= start2 and start1 <= end2) or (
            start2 >= start1 and start2 <= end1
        ):
            count += 1
    return count


# Read the pairs from the input file
with open("pairs.txt", "r") as f:
    pairs = f.readlines()

# Strip the newline characters from the pairs
pairs = [pair.strip() for pair in pairs]

# Print the number of overlapping pairs
print(find_overlapping_pairs(pairs))
