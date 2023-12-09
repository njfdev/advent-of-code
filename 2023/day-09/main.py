# read input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()


def predict_next(num_list, direction=1):
    # get the differences between each number
    differences = [num_list[i + 1] - num_list[i] for i in range(len(num_list) - 1)]

    # if all the differences are all 0, then return the last number in the list
    if all(difference == 0 for difference in differences):
        return num_list[0 - direction]

    if direction == 1:
        return num_list[-1] + predict_next(differences, direction=1)
    else:
        return num_list[0] - predict_next(differences, direction=0)


def parts(input, direction=1):
    total = 0

    for line in input:
        line = line.split(" ")
        line = [int(num) for num in line]
        total += predict_next(line, direction=direction)

    return total


print("(Part 1) Prediction Sum: ", parts(input_raw))
print("(Part 2) Prediction Sum: ", parts(input_raw, 0))
