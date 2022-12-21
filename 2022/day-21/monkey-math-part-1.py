from typing import List

# read monkeys.txt as a list of strings (strip newlines)
with open("monkeys.txt") as f:
    monkeys = [line.strip() for line in f]


class NumberMonkey:
    id: str
    number: int

    def __init__(self, id: str, number: int):
        self.id = id
        self.number = number


class OperationMonkey:
    id: str
    operation: List[str]

    def __init__(self, id: str, operation: List[str]):
        self.id = id
        self.operation = operation


numberMonkeys = []
operationMonkeys = []

for monkey in monkeys:
    monkey_str = monkey.split(" ")
    # id is the first element (strip the colon)
    monkey_id = monkey_str[0][:-1]

    if len(monkey_str) == 4:
        # operation monkey
        operationMonkeys.append(OperationMonkey(monkey_id, monkey_str[1:4]))
    else:
        # number monkey
        numberMonkeys.append(NumberMonkey(monkey_id, int(monkey_str[1])))

# find monkey with id "root" in operationMonkeys
root_monkey = [monkey for monkey in operationMonkeys if monkey.id == "root"][0]

# lets now use recursion
def getMonkeyValue(id: str):
    operationMonkey = [monkey for monkey in operationMonkeys if monkey.id == id]
    if len(operationMonkey) > 0:
        return solve_monkey(operationMonkey[0])
    else:
        return [monkey for monkey in numberMonkeys if monkey.id == id][0].number


def solve_monkey(monkey: OperationMonkey):
    [monkey1, operation, monkey2] = monkey.operation

    monkey1Value = getMonkeyValue(monkey1)
    monkey2Value = getMonkeyValue(monkey2)

    return eval("{}{}{}".format(monkey1Value, operation, monkey2Value))


print("Part 1 Solution:", int(solve_monkey(root_monkey)))
