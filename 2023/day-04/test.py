from functools import cache

with open("input.txt") as f:
    lines = f.readlines()


def score_card(l):
    _, body = l.split(":")
    win, bet = body.split("|")
    winners = set(win.strip().split())
    bettors = set(bet.strip().split())
    joined = winners & bettors
    print(joined)
    return len(joined)


score_table = [score_card(l) for l in lines]
total = sum([2 ** (s-1) for s in score_table])

print("Phase 1: ", total)


@cache
def count_cards(idx, depth=0):
    if idx >= len(score_table):
        return 0
    score = score_table[idx]
    if score == 0:
        return 1
    res = 1
    for i in range(score):
        res += count_cards(idx + i + 1, depth+1)
    return res


total_count = sum(count_cards(i) for i in range(len(score_table)))

print("Phase 2: ", total_count)