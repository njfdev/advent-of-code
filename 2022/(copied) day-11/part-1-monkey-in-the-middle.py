# read monkeys.txt
with open("monkeys.txt", "r") as f:
    # monkeys.txt is an array of arrays of strings
    # the top level array is split by double newlines
    # the second level array is split by single newlines
    raw_monkeys = f.read().split("\n\n")
    raw_list_monkeys = [monkey.split("\n") for monkey in raw_monkeys]
    # for each line in raw_list_monkeys, strip the whitespace
    raw_list_monkeys = [
        [line.strip() for line in monkey] for monkey in raw_list_monkeys
    ]


class Monkey:
    items = []
    operation = ""
    amount = 0
    modulus = 0
    true_monkey_index = 0
    false_monkey_index = 0
    inspections = 0

    def __init__(self, items, operation, test, true_result, false_result):
        # remove "Starting items: " from the beginning of items string and split by commas
        self.items = items.removeprefix("Starting items: ").split(", ")
        # remove "Operation: new = old " from the beginning of operation string and split by spaces
        # the first element is the operation, the second is the amount
        [self.operation, self.amount] = operation.removeprefix(
            "Operation: new = old "
        ).split(" ")
        # remove "Test: divisible by " from the beginning of test string and set modulus
        self.modulus = int(test.removeprefix("Test: divisible by "))
        # remove "If true: throw to monkey " from the beginning of true_result string and set true_monkey_index
        self.true_monkey_index = int(
            true_result.removeprefix("If true: throw to monkey ")
        )
        # remove "If false: throw to monkey " from the beginning of false_result string and set false_monkey_index
        self.false_monkey_index = int(
            false_result.removeprefix("If false: throw to monkey ")
        )


monkeys = []

for monkey in raw_list_monkeys:
    monkeys.append(
        Monkey(
            monkey[1],
            monkey[2],
            monkey[3],
            monkey[4],
            monkey[5],
        )
    )


def run_monkey_round():
    # for each monkey, inspect the items and perform the operation
    for monkey in monkeys:
        for item in monkey.items:
            # if monkey.amount is "old", set amount to item
            # if monkey.amount is an integer, set amount to amount
            if monkey.amount == "old":
                amount = int(item)
            else:
                amount = int(monkey.amount)

            # if operation is + = add, - = subtract, * = multiply, / = divide
            # set worry_level to item [operation] amount
            if monkey.operation == "+":
                worry_level = int(item) + amount
            elif monkey.operation == "-":
                worry_level = int(item) - amount
            elif monkey.operation == "*":
                worry_level = int(item) * amount
            elif monkey.operation == "/":
                worry_level = int(item) / amount

            # divide worry_level by 3 and round down
            worry_level = worry_level // 3
            # if worry_level is divisible by modulus, throw to true monkey
            if worry_level % monkey.modulus == 0:
                monkeys[monkey.true_monkey_index].items.append(worry_level)
            # else throw to false monkey
            else:
                monkeys[monkey.false_monkey_index].items.append(worry_level)

            # increment inspections
            monkey.inspections += 1

        # now that we looped through all the items, clear the monkey's items
        monkey.items = []


# run the monkey round 20 times
for i in range(20):
    run_monkey_round()

# get the 2 monkeys with the most inspections
monkeys.sort(key=lambda monkey: monkey.inspections, reverse=True)

# multiply the inspections of the 2 monkeys and print
print(
    "Level of the monkey buisness: "
    + str(monkeys[0].inspections * monkeys[1].inspections)
)
