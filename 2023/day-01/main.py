# read in input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()

# part 1

# use regex to remove non-numeric characters
import re

input = [re.sub("[^0-9]", "", i) for i in input_raw]

# get calibration sum
calibration_sum = 0

for i in input:
    # get the first and last alphanumeric characters, concatenate them, and add the resulting number to the sum
    calibration_sum += int(i[0] + i[len(i) - 1])

print("(Part 1) Sum of Calibration Values: " + str(calibration_sum))

# part 2

# find number text in input and replace with number
numbers = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

input = input_raw.copy()

# get regex to find numbers
regex = re.compile("(?=([0-9]|{}))".format("|".join(numbers)))

# get calibration sum
calibration_sum = 0

for i in input:
    # get the first and last number from the regex result
    regex_result = regex.findall(i)
    number = str(regex_result[0] + regex_result[len(regex_result) - 1])

    # replace number text with number
    for j in numbers:
        number = number.replace(j, str(numbers.index(j)))

    calibration_sum += int(number)

print("(Part 2) Sum of Calibration Values: " + str(calibration_sum))
