# Read the input data from a file
with open("rucksack-data.txt") as f:
    # read the lines into a list called rucksacks, make sure to strip the newline character
    rucksacks = [line.strip() for line in f.readlines()]

# Initialize a variable to store the sum of the item priorities
priority_sum = 0

rucksack_groups = [list(t) for t in zip(*[iter(rucksacks)] * 3)]

# Iterate over the list of rucksacks
for group in rucksack_groups:
    # Go through each group and find the common items
    common_items = set(group[0]).intersection(set(group[1])).intersection(set(group[2]))

    # Iterate over the common items and calculate their priority
    for item in common_items:
        # calculate the priority value based on the following
        # a-z = 1-26
        # A-Z = 27-52
        if item.islower():
            priority = ord(item) - ord("a") + 1
        else:
            priority = ord(item) - ord("A") + 27

        # Add the priority to the total sum
        priority_sum += priority

# Print the final sum of the item priorities
print(priority_sum)
