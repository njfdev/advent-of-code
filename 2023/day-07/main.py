# read input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()


from functools import cmp_to_key


hand_ranking = ["hc", "1p", "2p", "3", "fh", "4", "5"]
ranking = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

def get_hand_ranking(hand_counts):
    hand = "hc"

    counts_sorted = sorted(hand_counts.items(), key=lambda x: x[1], reverse=True)

    if counts_sorted[0][1] >= 4:
        hand = str(counts_sorted[0][1])
    elif counts_sorted[0][1] == 3 and counts_sorted[1][1] == 2:
        hand = "fh"
    elif counts_sorted[0][1] == 3:
        hand = "3"
    elif counts_sorted[0][1] == 2 and counts_sorted[1][1] == 2:
        hand = "2p"
    elif counts_sorted[0][1] == 2:
        hand = "1p"
    return hand_ranking.index(hand)


def get_hand_ranking_from_string(hand):
    cards = {}

    for i in hand:
        if i in cards:
            cards[i] += 1
        else:
            cards[i] = 1

    new_score = get_hand_ranking(cards)

    return new_score


def wildcard_ranking(hand):
    # get first instance of J
    try:
        j_index = hand.index("J")
    except ValueError:
        return get_hand_ranking_from_string(hand)

    best_score = 0
    for card in ranking[1:]:
        new_hand = hand[:j_index] + card + hand[j_index + 1:]
        best_score = max(wildcard_ranking(new_hand), best_score)

    return best_score


is_part2 = False

def compare_cards(a, b):
    a = a[0]
    b = b[0]

    a_hand = 0
    b_hand = 0

    if is_part2:
        a_hand = wildcard_ranking(a)
        b_hand = wildcard_ranking(b)
    else:
        a_hand = get_hand_ranking_from_string(a)
        b_hand = get_hand_ranking_from_string(b)
    

    if a_hand > b_hand:
        return 1
    elif a_hand < b_hand:
        return -1

    for i in range(len(a)):
        if ranking.index(a[i]) > ranking.index(b[i]):
            return 1
        elif ranking.index(a[i]) < ranking.index(b[i]):
            return -1
    
    return 0


def part1(input):
    input = [i.split(" ") for i in input]

    input = sorted(input, key=cmp_to_key(compare_cards))

    score = 0

    for i, hand in enumerate(input):
        score += (i + 1) * int(hand[1])

    return score


def part2(input):
    # move J to the start of the ranking
    ranking.insert(0, ranking.pop(ranking.index("J")))
    global is_part2
    is_part2 = True
    return part1(input)


print("(Part 1) Cards multiplied by ranking: ", part1(input_raw))
print("(Part 2) Cards multiplied by ranking with wildcards: ", part2(input_raw))
