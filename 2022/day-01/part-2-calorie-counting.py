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

# get variable to store the amount of calories carried by each of the top 3 elves
top_calories = sorted(calories, reverse=True)[:3]

# we now print the amount of calories carried by each of the top 3 elves
print("Amount of calories carried by each of the top 3 elves: {}".format(top_calories))

# finally, we print the total amount of calories carried by the top 3 elves
print("Total amount of calories carried by the top 3 elves: {}".format(sum(top_calories)))