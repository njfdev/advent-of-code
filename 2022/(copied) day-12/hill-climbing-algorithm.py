import collections, string


class SquareGrid:
    def __init__(self, labels):
        self.labels = labels
        self.width = len(labels[0])
        self.height = len(labels)

    def label_from_node(self, node):
        if not node:
            return "#"
        else:
            col, row = node
            return self.labels[row][col]

    def node_from_label(self, label):
        for row_i in range(self.height):
            if label in self.labels[row_i]:
                return (self.labels[row_i].index(label), row_i)

    def in_bounds(self, node):
        x, y = node
        return 0 <= x < self.width and 0 <= y < self.height

    def too_high(self, node1, node2):
        label1 = self.label_from_node(node1)
        label2 = self.label_from_node(node2)
        if self.label_from_node(node2) == "E":
            label2 = "z"
        height1 = string.ascii_letters.index(label1)
        height2 = string.ascii_letters.index(label2)
        return height2 - height1 > 1

    def neighbors(self, node):
        x, y = node
        new_nodes = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        neighbors = []
        for new_node in new_nodes:
            if self.in_bounds(new_node):
                neighbors.append(new_node)
        return neighbors


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return not self.elements

    def add(self, element):
        self.elements.append(element)

    def get(self):
        return self.elements.popleft()


def breadth_first_search(grid, start, end):
    frontier = Queue()
    frontier.add(start)
    came_from = {}
    came_from[start] = None
    steps = 0
    while not frontier.empty():
        current_node = frontier.get()
        if current_node == end:
            break
        for next_node in grid.neighbors(current_node):
            if next_node not in came_from and not grid.too_high(
                current_node, next_node
            ):
                steps += 1
                came_from[next_node] = current_node
                frontier.add(next_node)
    return came_from


def part1_solution(day12_input):
    solution = []
    grid = SquareGrid(day12_input)
    start = grid.node_from_label("S")
    end = grid.node_from_label("E")
    path = breadth_first_search(grid, start, end)
    node = end
    while node != start:
        solution.append(grid.label_from_node(path[node]))
        node = path[node]
    return solution


def part2_solution(day12_input):
    solution = []
    paths = []
    grid = SquareGrid(day12_input)
    start_nodes = []
    for row_i in range(len(grid.labels)):
        for col_i in range(len(grid.labels[row_i])):
            if grid.labels[row_i][col_i] == "a" or grid.labels[row_i][col_i] == "S":
                start_nodes.append((col_i, row_i))
    end = grid.node_from_label("E")
    for start_node in start_nodes:
        path = []
        searched = breadth_first_search(grid, start_node, end)
        if end in searched:
            node = end
            while node != start_node:
                path.append(searched[node])
                node = searched[node]
            paths.append(path)
    solution = [len(p) for p in paths]
    solution.sort()
    return solution[0]


with open("elevations.txt", "r", encoding="UTF-8") as f:
    day12_input = [list(line) for line in f.read().split("\n")]

print(f"Part1: {len(part1_solution(day12_input))}")
print(f"Part2: {part2_solution(day12_input)}")
