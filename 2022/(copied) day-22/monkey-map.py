import time
import re


class Interval:
    def __init__(self, l, r):
        if r <= l:
            r = l

        self.l = l
        self.r = r

    def get_overlap(self, other):
        return Interval(max(self.l, other.l), min(self.r, other.r))

    def is_empty(self):
        return self.l >= self.r

    def length(self):
        return self.r - self.l

    def get_range(self):
        return range(self.l, self.r)

    def includes(self, x):
        return x >= self.l and x < self.r

    def subtract(self, other, focus):
        left = Interval(self.l, min(self.r, other.l))
        right = Interval(max(self.l, other.r), self.r)
        if left.length() + right.length() + other.length() != self.length():
            print("PANIK A")

        if left.includes(focus):
            return left
        return right


class Node:
    def __init__(self, row, col, wall=False, l=None):
        self.r = None
        self.u = None
        self.d = None
        self.l = l
        if not self.l is None:
            self.l.r = self

        self.wall = wall

        self.coords = (row, col)

        self.d_map = {direction: 1 for direction in ["r", "l", "u", "d"]}

    def set_r(n, val, d):
        n.r = val
        n.d_map["r"] = d

    def set_u(n, val, d):
        n.u = val
        n.d_map["u"] = d

    def set_d(n, val, d):
        n.d = val
        n.d_map["d"] = d

    def set_l(n, val, d):
        n.l = val
        n.d_map["l"] = d

    def move(self, d, ignore_walls=False):
        if d.real > 0:
            goal = self.r
            d_mod = self.d_map["r"]
        elif d.real < 0:
            goal = self.l
            d_mod = self.d_map["l"]
        elif d.imag > 0:
            goal = self.u
            d_mod = self.d_map["u"]
        elif d.imag < 0:
            goal = self.d
            d_mod = self.d_map["d"]

        if goal.wall and not ignore_walls:
            return None, d

        return goal, d_mod * d

    def zip_nodes(self, lower, amount):
        self.d = lower
        lower.u = self

        if amount > 1:
            self.r.zip_nodes(lower.r, amount - 1)

    def zip_edge(self, other, amount, self_set, other_set, self_dir, other_dir, d_mod):
        self_set(self, other, d_mod)
        other_set(other, self, 1 / d_mod)

        if amount > 1:
            self.move(self_dir, True)[0].zip_edge(
                other.move(other_dir, True)[0],
                amount - 1,
                self_set,
                other_set,
                self_dir,
                other_dir,
                d_mod,
            )

    def find_column(self, column, start):
        if self.coords[1] == column:
            return self
        if self.r == start:
            print("PANIK B")
            return None
        return self.r.find_column(column, start)

    def find_first_missing(self, start):
        if self.u is None:
            return self
        if self.r != start:
            return self.r.find_first_missing(start)
        return None


def d22p1(file) -> int:
    with open(file) as f:
        lines = f.readlines()

    rows = []

    for i, l in enumerate(lines):
        if l == "\n":
            break
        first = None
        last = None
        off = l.count(" ")
        for j, c in enumerate(l.strip()):
            n = Node(i, off + j, c == "#", last)
            first = first or n
            last = n
        last.r = first
        first.l = last
        rows.append((first, Interval(off, l.count(" ") + len(l.strip()))))

    for i, (f, iv) in enumerate(rows):
        while not f.find_first_missing(f) is None:
            f_m = f.find_first_missing(f)
            iv_now = Interval(f_m.coords[1], iv.r)
            j = (i - 1) % len(rows)
            while True:
                ov = iv_now.get_overlap(rows[j][1])
                if ov.includes(f_m.coords[1]):
                    su = rows[j][0].find_column(ov.l, rows[j][0])
                    sl = f_m.find_column(ov.l, f_m)
                    su.zip_nodes(sl, ov.length())
                    break
                elif not ov.is_empty():
                    iv_now = iv_now.subtract(ov, f_m.coords[1])
                j = (j - 1) % len(rows)

    d = 1 + (0 * 1j)
    d_v = 0
    curr = rows[0][0]

    for command in re.split("(\d+)", lines[-1])[1:-1]:
        if command == "R":
            d = d * (-1 * 1j)
            d_v = (d_v + 1) % 4
            continue
        if command == "L":
            d = d * 1j
            d_v = (d_v - 1) % 4
            continue

        for _ in range(int(command)):
            nex, d = curr.move(d)
            if nex is None:
                break
            curr = nex

    return (curr.coords[0] + 1) * 1000 + (curr.coords[1] + 1) * 4 + d_v


def d22p2(file) -> int:
    def make_edge(rows, ps, px, py, cx, cy, sx, sy, dx, dy, dm):
        x_coord = (
            px[0] * ps + max(0, (cx[0] * ps) - 1),
            px[1] * ps + max(0, (cx[1] * ps) - 1),
        )
        y_coord = (
            py[0] * ps + max(0, (cy[0] * ps) - 1),
            py[1] * ps + max(0, (cy[1] * ps) - 1),
        )
        x = rows[x_coord[0]][0].find_column(x_coord[1], rows[x_coord[0]][0])
        y = rows[y_coord[0]][0].find_column(y_coord[1], rows[y_coord[0]][0])
        x.zip_edge(y, ps, sx, sy, dx, dy, dm)

    with open(file) as f:
        lines = f.readlines()

    rows = []

    for i, l in enumerate(lines):
        if l == "\n":
            break
        first = None
        last = None
        off = l.count(" ")
        for j, c in enumerate(l.strip()):
            n = Node(i, off + j, c == "#", last)
            first = first or n
            last = n
        rows.append((first, Interval(off, l.count(" ") + len(l.strip()))))

    for i, (fu, iu) in enumerate(rows[:-1]):
        fl, il = rows[i + 1]
        ov = iu.get_overlap(il)
        su = fu.find_column(ov.l, fu)
        sl = fl.find_column(ov.l, fl)
        su.zip_nodes(sl, ov.length())

    if "b" not in file:
        size = 50
        A = (0, 1)
        B = (0, 2)
        C = (1, 1)
        D = (2, 0)
        E = (2, 1)
        F = (3, 0)

        top_left = (0, 0)
        top_right = (0, 1)
        bot_left = (1, 0)
        bot_right = (1, 1)

        # A to D
        make_edge(
            rows, size, A, D, top_left, bot_left, Node.set_l, Node.set_l, -1j, 1j, -1
        )

        # A to F
        make_edge(
            rows, size, A, F, top_left, top_left, Node.set_u, Node.set_l, 1, -1j, -1j
        )

        # B to F
        make_edge(rows, size, B, F, top_left, bot_left, Node.set_u, Node.set_d, 1, 1, 1)

        # B to E
        make_edge(
            rows, size, B, E, top_right, bot_right, Node.set_r, Node.set_r, -1j, 1j, -1
        )

        # B to C
        make_edge(
            rows, size, B, C, bot_left, top_right, Node.set_d, Node.set_r, 1, -1j, -1j
        )

        # C to D
        make_edge(
            rows, size, C, D, top_left, top_left, Node.set_l, Node.set_u, -1j, 1, 1j
        )

        # E to F
        make_edge(
            rows, size, E, F, bot_left, top_right, Node.set_d, Node.set_r, 1, -1j, -1j
        )
    else:
        size = 4
        A = (0, 2)
        B = (1, 0)
        C = (1, 1)
        D = (1, 2)
        E = (2, 2)
        F = (2, 3)

        top_left = (0, 0)
        top_right = (0, 1)
        bot_left = (1, 0)
        bot_right = (1, 1)

        # A to B
        make_edge(
            rows, size, A, B, top_left, top_right, Node.set_u, Node.set_u, 1, -1, -1
        )

        # A to C
        make_edge(
            rows, size, A, C, top_left, top_left, Node.set_l, Node.set_u, -1j, 1, 1j
        )

        # A to F
        make_edge(
            rows, size, A, F, top_right, bot_right, Node.set_r, Node.set_r, -1j, 1j, -1
        )

        # B to E
        make_edge(
            rows, size, B, E, bot_left, bot_right, Node.set_d, Node.set_d, 1, -1, -1
        )

        # B to F
        make_edge(
            rows, size, B, F, top_left, bot_right, Node.set_l, Node.set_d, -1j, -1, -1j
        )

        # C to E
        make_edge(
            rows, size, C, E, bot_left, bot_left, Node.set_d, Node.set_l, 1, 1j, 1j
        )

        # D to F
        make_edge(
            rows, size, D, F, bot_right, top_left, Node.set_r, Node.set_u, 1j, 1, -1j
        )

    for f, iv in rows:
        curr = f
        while curr.coords[0] == f.coords[0]:
            if curr.u is None or curr.l is None or curr.d is None or curr.r is None:
                breakpoint()
            curr = curr.r

    d = 1 + (0 * 1j)
    d_v = {1: 0, -1: 2, 1j: 3, -1j: 1}
    curr = rows[0][0]

    planes = [["", "A", "B"], ["", "C", ""], ["D", "E", ""], ["F", "", ""]]
    to_plane = lambda r, c: planes[int(r / 50)][int(c / 50)]

    for command in re.split("(\d+)", lines[-1])[1:-1]:
        if command == "R":
            d = d * (-1 * 1j)
            continue
        if command == "L":
            d = d * 1j
            continue

        for _ in range(int(command)):
            nex, d_nex = curr.move(d)
            if nex is None:
                break

            if abs(curr.coords[0] - nex.coords[0]) > 1:
                if "b" not in file:
                    curr_plane = to_plane(curr.coords[0], curr.coords[1])
                    nex_plane = to_plane(nex.coords[0], nex.coords[1])
                # print(f"Curr: {curr.coords}, Next: {nex.coords}, Dir: {d}, Next Dir: {d_nex}")
                # breakpoint()

            curr = nex
            d = d_nex

    return (curr.coords[0] + 1) * 1000 + (curr.coords[1] + 1) * 4 + d_v[d]


file = "monkey-notes.txt"
start = time.time()
print(d22p1(file))
middle = time.time()
print(d22p2(file))
end = time.time()

print(f"Part 1 runs in {middle - start}s")
print(f"Part 2 runs in {end - middle}s")
