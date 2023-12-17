import heapq


def minimal_heat(start, end, least, most):
    queue = [(0, *start, 0, 0)]
    seen = set()
    while queue:
        heat, x, y, px, py = heapq.heappop(queue)
        if (x, y) == end:
            return heat
        if (x, y, px, py) in seen:
            continue
        seen.add((x, y, px, py))
        # calculate turns only
        for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)} - {(px, py), (-px, -py)}:
            a, b, h = x, y, heat
            # enter 4-10 moves in the chosen direction
            for i in range(1, most + 1):
                a, b = a + dx, b + dy
                if (a, b) in board:
                    h += board[a, b]
                    if i >= least:
                        heapq.heappush(queue, (h, a, b, dx, dy))


board = {
    (i, j): int(c)
    for i, r in enumerate(open("input.txt"))
    for j, c in enumerate(r.strip())
}

# I tried for a while with A*, but I spent too much time working on it, so this is a copied solution
print("(Copied - Part 1): ", minimal_heat((0, 0), max(board), 1, 3))
print("(Copied - Part 2): ", minimal_heat((0, 0), max(board), 4, 10))
