# read in input.txt
with open("input.txt", "r") as f:
    data = f.read().strip().split(",")


def hash_algo(value, char):
    # get ascii value of char
    ascii_value = ord(char)

    current_value = value + ascii_value

    return (current_value * 17) % 256


def calculate_hash(string):
    value = 0
    for char in string:
        value = hash_algo(value, char)
    return value


def part1(data):
    return sum([calculate_hash(string) for string in data])


def apply_step(instruction, boxes):
    new_boxes = boxes.copy()

    if "=" in instruction:
        label, value = instruction.split("=")
        box_index = calculate_hash(label)

        # if label is in box index in the first element of any of its lists
        if any(lens[0] == label for lens in new_boxes[box_index]):
            # find the list that has the label in the first element
            for i in range(len(new_boxes[box_index])):
                if new_boxes[box_index][i][0] == label:
                    # change the value
                    new_boxes[box_index][i][1] = str(value)
                    break
        else:
            new_boxes[box_index].append([label, str(value)])
    elif instruction[-1] == "-":
        box_index = calculate_hash(instruction[:-1])
        # if there is a list with the label in the first element
        if any(lens[0] == instruction[:-1] for lens in new_boxes[box_index]):
            # find the list that has the label in the first element
            for i in range(len(new_boxes[box_index])):
                if new_boxes[box_index][i][0] == instruction[:-1]:
                    # remove the list
                    new_boxes[box_index].pop(i)
                    break

    return new_boxes


def part2(data):
    boxes = [[] for _ in range(256)]

    for i in range(len(data)):
        boxes = apply_step(data[i], boxes)

    # calculate focusing power
    focusing_power = 0

    for i, box in enumerate(boxes):
        for j, instruction in enumerate(box):
            focusing_power += (i + 1) * (j+1) * int(instruction[1])

    return focusing_power


# this one seemed very easy to me
print("(Part 1) HASH sum: ", part1(data))
print("(Part 2) Focusing power: ", part2(data))