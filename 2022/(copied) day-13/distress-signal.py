import json

with open("signal.txt") as text_file:
    pairs_one = [x.strip().split("\n") for x in text_file.read().strip().split("\n\n")]
    text_file.seek(0)
    pairs_two = list(
        map(json.loads, filter(None, text_file.read().strip().split("\n")))
    )


def compare(p1, p2, lenl, lenr):
    while True:
        try:
            l, r = next(p1), next(p2)
        except StopIteration:
            if lenl == lenr:
                return
            return True if lenl < lenr else False
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return True
            if l > r:
                return False
        elif isinstance(l, list) and isinstance(r, list):
            res = compare(iter(l), iter(r), len(l), len(r))
            if res is not None:
                return res
        elif (isinstance(l, list) and isinstance(r, int)) or (
            isinstance(l, int) and isinstance(r, list)
        ):
            if isinstance(l, int):
                res = compare(iter([l]), iter(r), 1, len(r))
            else:
                res = compare(iter(l), iter([r]), len(l), 1)
            if res is not None:
                return res


# Part 1
correct_order = list()
for i, p in enumerate(pairs_one):
    p1, p2 = json.loads(p[0]), json.loads(p[1])
    correct_order.append(i + 1 if compare(iter(p1), iter(p2), len(p1), len(p2)) else 0)
print(sum(correct_order))  # Part 1 result

# Part 2
div1, div2 = [[[2]], [[6]]]
pairs_two.extend([div1, div2])
prev = list()
while True:
    if pairs_two == prev:
        break
    prev = pairs_two.copy()
    for i in range(len(pairs_two) - 1):
        l, r = pairs_two[i], pairs_two[i + 1]
        res = compare(
            iter(pairs_two[i]),
            iter(pairs_two[i + 1]),
            len(pairs_two[i]),
            len(pairs_two[i + 1]),
        )
        if not res:
            pairs_two[i] = r
            pairs_two[i + 1] = l
print((pairs_two.index(div1) + 1) * (pairs_two.index(div2) + 1))  # Part 2 result
