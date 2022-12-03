# Read the input data from a file
with open("rucksack-data.txt") as f:
    rucksacks = f.readlines()

# Initialize a variable to store the sum of the item priorities
priority_sum = 0

# Iterate over the list of rucksacks
for rucksack in rucksacks:
    # Split the rucksack into two compartments
    comp1, comp2 = rucksack[: len(rucksack) // 2], rucksack[len(rucksack) // 2 :]

    # Initialize a set to store the items in each compartment
    items1 = set()
    items2 = set()

    # Iterate over the items in each compartment and add them to the sets
    for item in comp1:
        items1.add(item)
    for item in comp2:
        items2.add(item)

    # Find the items that appear in both compartments by taking the intersection of the two sets
    common_items = items1.intersection(items2)

    # Iterate over the common items and calculate their priority
    for item in common_items:
        # If the item is lowercase, its priority is ord(item) - ord('a') + 1
        # If the item is uppercase, its priority is ord(item) - ord('A') + 27
        if item.islower():
            priority = ord(item) - ord("a") + 1
        else:
            priority = ord(item) - ord("A") + 27

        # Add the priority to the total sum
        priority_sum += priority

# Print the final sum of the item priorities
print(priority_sum)
