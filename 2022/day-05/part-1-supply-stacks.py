# read the stack-data.txt file into the raw_data variable
with open("stack-data.txt", "r") as f:
    # make sure to strip the last 2 characters from each line
    raw_data = f.readlines()

# our raw data contains 2 sections, the first is the stack data, the second is the instructions
# we can split the data by finding the empty line
split_index = raw_data.index("\n")
raw_stack_data = [line[:-1] for line in raw_data[:split_index]]
instructions = [line.strip() for line in raw_data[split_index + 1 :]]

# we now need to parse the raw stack data into a list of stacks
# the data is formatted as follows:
# [N]
# [W]     [P]
# [S] [E] [Y]
#  1   2   3
# letters inside the square brackets are the identifiers
# the numbers are the stack numbers
# we can use this to create an array of stacks ordered by stack number
# the top crate in the stack should be the last crate in the array
# the bottom crate in the stack should be the first crate in the array
# create an empty list of lists with a length of the number of "[" characters in the 2nd to last line of raw_stack_data
stack_data = [[] for _ in range(0, raw_stack_data[-2].count("["))]
# we can ignore the last line of data because it is redundant (we already know the index based on the order)
# we should also start at the 2nd to last line and work backwards
for line in raw_stack_data[-2::-1]:
    # split the line at every 3 characters and skip the following character
    raw_crates = [line[i : i + 3] for i in range(0, len(line), 4)]
    # we now want to remove the square brackets from the crate identifiers
    # we can do this by removing the first and last characters from each crate identifier
    crates = [crate[1:-1] for crate in raw_crates]
    # we now want to add the crates to the stack_data array
    # we do this by adding the crates to the stack_data array at the index of the stack identifier
    # loop through each crate index
    for crate_index, crate in enumerate(crates):
        if crate == " " or crate == "":
            continue
        # we can add the crate to the stack_data array
        stack_data[crate_index].append(crate)

# we now need to parse the instructions
# the instructions are formatted as follows:
# move [amount] from [stack] to [stack]
# we should go through each instruction and perform the move in order
for instruction in instructions:
    # split the instruction to get the parts
    parts = instruction.split()
    # we can get the amount by converting the second part to an integer
    amount = int(parts[1])
    # we can get the source stack number by converting the fourth part to an integer
    source_stack_number = int(parts[3]) - 1
    # we can get the destination stack number by converting the sixth part to an integer
    destination_stack_number = int(parts[5]) - 1

    # get the last [amount] crates from the source stack and reverse the order
    moved_crates = stack_data[source_stack_number][-amount:][::-1]
    # remove the last [amount] crates from the source stack
    stack_data[source_stack_number] = stack_data[source_stack_number][:-amount]
    # add the moved crates to the destination stack
    stack_data[destination_stack_number] += moved_crates

# we now need to print the top crate in each stack
# we can do this by going through each stack in the stack_data array
for stack in stack_data:
    if len(stack) > 0:
        # we can print the top crate by printing the last crate in the stack
        print(stack[-1], end="")

print()
