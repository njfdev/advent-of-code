# read input.txt
with open("input.txt", "r") as f:
    data_split = f.read().split("\n\n")


def parse_data(data_list):
    rules_raw = data_list[0].splitlines()
    parts_raw = data_list[1].splitlines()

    rules = {}

    for rule in rules_raw:
        rules[rule.split("{")[0].strip()] = [condition.split(":") for condition in rule.split("{")[1].split("}")[0].split(",")]

    parts = []

    for part in parts_raw:
        split_part = part[1:len(part)-1].split(",")

        parts.append({
            "x": int(split_part[0][2:]),
            "m": int(split_part[1][2:]),
            "a": int(split_part[2][2:]),
            "s": int(split_part[3][2:]),
        })

    return rules, parts


def calculate_value(part, rules, current_rule = None):
    if current_rule is None:
        current_rule = rules["in"]

    while True:
        for condition in current_rule:
            next_rule = None
            if len(condition) == 1:
                next_rule = condition[0].strip()
            elif ">" in condition[0]:
                if part[condition[0].split(">")[0].strip()] > int(condition[0].split(">")[1].strip()):
                    next_rule = condition[1].strip()
                else:
                    continue
            elif "<" in condition[0]:
                if part[condition[0].split("<")[0].strip()] < int(condition[0].split("<")[1].strip()):
                    next_rule = condition[1].strip()
                else:
                    continue

            if next_rule == "A":
                return part["x"] + part["m"] + part["a"] + part["s"]
            if next_rule == "R":
                return 0
            current_rule = rules[next_rule]
            break
      

def part1(input):
    rules, parts = parse_data(input)

    return sum([calculate_value(part, rules) for part in parts])


print("(Part 1) Total Rating Numbers: ", str(part1(data_split)))


# not my code
from copy import deepcopy
def generate_Lambda(flow):  # wel sad this is to good for part 2
    flow = flow.split(",")
    lambdastr = "lambda x, m, a, s: "
    for f in flow:
        if ":" in f:
            condition, label = f.split(':')
            lambdastr += "'" + label + "' if " + condition + " else "
        else:
            lambdastr += "'" + f + "'"
    return eval(lambdastr)


lambdadict = {}
stringdict = {}
with open('input.txt') as f:
    flows, parts = f.read().split("\n\n")
    parts = [
        eval(part.replace("=", ":").replace("x", "'x'").replace("m", "'m'").replace("a", "'a'").replace("s", "'s'")) for
        part in parts.split("\n")]
    for flow in flows.split("\n"):
        name, function = flow.split("{")
        lambdadict[name] = generate_Lambda(function[:-1])
        stringdict[name] = function[:-1].split(",")

def end_sum(xmas):
    m = 1
    for s, e in xmas.values():
        m *= (e - s + 1)
    return m

def recursive_range_run(xmas, flowname):
    rangesum = 0
    for condition in stringdict[flowname]:
        if ":" in condition:
            con, to = condition.split(":")
            if ">" in con:
                val, num = con.split(">")
                newXmas = deepcopy(xmas)
                if newXmas[val][1] > int(num):
                    newXmas[val][0] = max(xmas[val][0], int(num) + 1)
                    if to == "A":
                        rangesum += end_sum(newXmas)
                    elif to != "R":
                        rangesum += recursive_range_run(newXmas, to)
                    xmas[val][1] = min(xmas[val][1], int(num))
            if "<" in con:
                val, num = con.split("<")
                newXmas = deepcopy(xmas)
                if newXmas[val][0] < int(num):
                    newXmas[val][1] = min(xmas[val][1], int(num) - 1)
                    if to == "A":
                        rangesum += end_sum(newXmas)
                    elif to != "R":
                        rangesum += (recursive_range_run(newXmas, to))
                    xmas[val][0] = max(xmas[val][0], int(num))
        else:
            if condition == "A":
                rangesum += end_sum(xmas)
            elif condition != "R":
                rangesum += recursive_range_run(xmas, condition)
    return rangesum

print("(Copied - Part 2) Total Distinct Number Ratings: ",
      recursive_range_run({"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}, "in"))
