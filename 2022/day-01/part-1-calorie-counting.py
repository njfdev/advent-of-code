# read data from calories.txt and save it to raw_calories
with open('calories.txt', 'r') as f:
    raw_calories = f.read()

# create variable to store calories starting at 0
calories = [0]

# loop through raw_calories
index = 0
for line in raw_calories.split('\n'):
    # if line is a number, increase calories by that number at index
    # otherwise, add 1 to index and append 0 to calories
    if line.isnumeric():
        calories[index] += int(line)
    else:
        index += 1
        calories.append(0)

# now that we have the total amount of calories for each elf, we can find the max
print("Most calories carried by a single elf: {}".format(max(calories)))