# read in instructions.txt as a list of strings called instructions
with open("instructions.txt") as f:
    # make sure to strip the newline character
    instructions = [line.strip() for line in f.readlines()]

# create variable cycle_count
cycle_count = 0
# create signal_strength variable
signal_strength = 0
# create x_register variable
x_register = 1

current_horizontal = 0


def check_cycle_count(cycle_count):
    global signal_strength
    if cycle_count in [20, 60, 100, 140, 180, 220]:
        signal_strength += cycle_count * x_register

    draw_pixel(cycle_count)


def draw_pixel(cycle_count):
    global current_horizontal

    if cycle_count % 40 in [i + x_register + 1 for i in range(-1, 1 + 1)]:
        print("#", end=" ")
    else:
        print(".", end=" ")

    if int(cycle_count / 40) - 1 == current_horizontal:
        print("")
        current_horizontal += 1


# loop through instructions
for instruction in instructions:
    # if instruction is "noop", increment cycle_count by 1
    if instruction == "noop":
        cycle_count += 1
        check_cycle_count(cycle_count)
    # if the instruction is addx, increment cycle_count by 2 and add instruction parameter to x_register
    elif instruction.startswith("addx"):
        cycle_count += 2
        check_cycle_count(cycle_count - 1)
        check_cycle_count(cycle_count)
        x_register += int(instruction.split()[1])

# print signal_strength
print(signal_strength)
