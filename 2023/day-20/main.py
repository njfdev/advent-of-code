# read input.txt
with open("input.txt", "r") as f:
    data = f.read().splitlines()


total_high_pulse = 0
total_low_pulse = 0

modules = {}
calls_to_process = []

is_part2 = False

class FlipFlop:
    def __init__(self, inputs, outputs, key):
        self.state = False
        self.inputs = inputs
        self.outputs = outputs
        self.key = key

    def __call__(self, pulse: bool, input_name: str):
        # if pulse is falsey
        if not pulse:
            self.state = not self.state
            to_add = []
            for output in self.outputs:
                if not self.state:
                    global total_low_pulse
                    total_low_pulse += 1
                elif self.state:
                    global total_high_pulse
                    total_high_pulse += 1
                if output not in modules.keys():
                    if output == "rx" and not self.state and is_part2:
                        raise Exception("rx")
                    continue
                #modules[output](self.state, module_index)
                to_add.append((output, self.state, self.key))
            return to_add


class Conjunction:
    def __init__(self, inputs, outputs, key):
        self.inputs = inputs
        self.last_input_states = {}
        self.outputs = outputs
        self.key = key

    def __call__(self, pulse: bool, input_name: str):
        self.last_input_states[input_name] = pulse
        to_add = []
        if all(self.last_input_states.values()):
            for output in self.outputs:
                global total_low_pulse
                total_low_pulse += 1
                if output not in modules.keys():
                    if output == "rx" and is_part2:
                        raise Exception("rx")
                    continue
                #modules[output](False, modules.get(self))
                to_add.append((output, False, self.key))
        else:
            for output in self.outputs:
                global total_high_pulse
                total_high_pulse += 1
                if output not in modules.keys():
                    continue
                #modules[output](True, modules.get(self))
                to_add.append((output, True, self.key))
        return to_add



class Broadcaster:
    def __init__(self, outputs, key):
        self.outputs = outputs
        self.key = key

    def __call__(self):
        global total_low_pulse
        total_low_pulse += 1

        # if pulse is falsey
        for output in self.outputs:
            total_low_pulse += 1
            calls_to_process.extend(modules[output](False, self.key))
        
        while calls_to_process:
            to_add = []
            for _ in range(len(calls_to_process)):
                output, pulse, module = calls_to_process.pop(0)
                next_calls = modules[output](pulse, module)
                if next_calls:
                    to_add.extend(next_calls)
            calls_to_process.extend(to_add)


def setup_modules(input):
    global total_high_pulse, total_low_pulse, modules, calls_to_process

    total_high_pulse = 0
    total_low_pulse = 0

    modules = {}
    calls_to_process = []

    # parse input
    for line in input:
        line_data = line.split(" -> ")
        output_strings = line_data[1].split(", ")
        if "broadcaster" in line_data[0]:
            modules["broadcaster"] = Broadcaster(output_strings, "broadcaster")
        elif "%" in line_data[0]:
            modules[line_data[0][1:]] = FlipFlop([], output_strings, line_data[0][1:])
        elif "&" in line_data[0]:
            modules[line_data[0][1:]] = Conjunction([], output_strings, line_data[0][1:])

    # go through outputs of each modules and add it to corresponding module inputs
    for key, _ in modules.items():
        for output in modules[key].outputs:
            if output not in modules.keys():
                continue
            modules[output].inputs.append(key)
    
    # go through all conjunctions and set last_input_states to False
    for key, _ in modules.items():
        if isinstance(modules[key], Conjunction):
            modules[key].last_input_states = {input_name: False for input_name in modules[key].inputs}


def part1(input):
    setup_modules(input)
    
    global total_low_pulse
    global total_high_pulse

    total_pulses = [0, 0]
    # call broadcaster
    for i in range(1000):
        modules["broadcaster"]()
        total_pulses[0] += total_low_pulse
        total_pulses[1] += total_high_pulse
        total_low_pulse = 0
        total_high_pulse = 0

    return total_pulses[0] * total_pulses[1]


def part2(input):
    setup_modules(input)

    global is_part2
    is_part2 = True

    button_presses = 0
    
    while True:
        try:
            button_presses += 1
            print(button_presses, end="\r")
            modules["broadcaster"]()
        except Exception as e:
            if str(e) == "rx":
                break
            else:
                raise e

    return button_presses


print("(Part 1) Low x High Pulse: ", part1(data))
# Theoretically this should work, but it takes too long to run
#print("(Part 2) Button Presses: ", part2(data))

# not my code
import re
import math


class Node:
    def __init__(self, type, toward):
        self.to = toward
        self.type = type
        self.state = False
        self.last = {}

    def set_before(self, before):
        if self.type == "conjunction":
            for b in before:
                self.last[b] = 0
            # print(self.last)

    def send_signal(self, before, input):
        # print(self.type)
        if self.type == "broadcaster":
            return [(t, 0) for t in self.to]
        if self.type == "flip_flop":
            if input == 0:
                if self.state:
                    output = [(t, 0) for t in self.to]
                else:
                    output = [(t, 1) for t in self.to]
                self.state = not self.state
            else:
                output = []
            return output
        if self.type == "conjunction":
            self.last[before] = input
            # print(self.last)
            if all(p == 1 for p in self.last.values()):
                output = [(t, 0) for t in self.to]
            else:
                output = [(t, 1) for t in self.to]
            return output

    def original_state(self):
        if self.type == "broadcaster":
            return True
        if self.type == "flip_flop":
            return self.state is False
        if self.type == "conjunction":
            return all(p == 0 for p in self.last.values())

    def back_to_default(self):
        if self.type == "flip_flop":
            self.state = False
        if self.type == "conjunction":
            self.last = {key: 0 for key in self.last}

class Graph:
    def __init__(self, lines):
        self.graph = {}
        self.state = {}

        tofrom = {}
        for s, to in lines:
            name = "".join(re.findall("[a-zA-Z]+", s))
            if s[0] == "%":
                self.graph[name] = Node("flip_flop", to.split(", "))
            elif s[0] == "&":
                self.graph[name] = Node("conjunction", to.split(", "))
            else:
                self.graph[name] = Node("broadcaster", to.split(", "))
            tofrom[name] = to.split(", ")

        self.fromto = {}
        for k, v in tofrom.items():
            for x in v:
                self.fromto.setdefault(x, []).append(k)
        # print(self.fromto)

        for name, before in self.fromto.items():
            if name in self.graph.keys():
                self.graph[name].set_before(before)


    def find_cycle(self, max ,pt1, to, pt2):
        high, low, cycle = 0, 0, 0
        while (not all(value.original_state() for value in self.graph.values()) or cycle == 0):

            Queue = [("button", "broadcaster", 0)]
            low += 1
            while Queue:
                last, current, signal = Queue.pop(0)
                if pt2 and current == to and signal == 0:
                    return cycle+1
                if current not in self.graph.keys():
                    continue
                next = self.graph[current].send_signal(last, signal)
                for n, s in next:
                    Queue.append((current, n, s))
                    if s == 0:
                        low += 1
                    else:
                        high += 1
            cycle += 1
            if pt1 and cycle == max:
                break

        return high, low, cycle

    def click_button(self, times):
        h, l, c = self.find_cycle(1000, True, "", False)
        return (h * (times//c)) * (l * (times//c))

    def find_low(self, node):
        for value in self.graph.values():
            value.back_to_default()
        sender = self.fromto[node]
        dependson = self.fromto[sender[0]]
        subcycles = []
        for d in dependson:
            for value in self.graph.values():
                value.back_to_default()
            c = self.find_cycle(1, False, d, True)
            subcycles.append(c)
        return math.lcm(*subcycles)




with open('input.txt') as f:
    lines = f.read().splitlines()
    lines = [line.split(" -> ") for line in lines]

Network = Graph(lines)
print("(Copied - Part 2) Button Presses: ", Network.find_low("rx"))