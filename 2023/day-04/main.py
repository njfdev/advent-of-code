# read in input.txt
with open("input.txt", "r") as f:
    data = f.read().splitlines()

def part1(input):
    total = 0
    for card in input:
        info = card.split(": ")[1]
        info = info.split(" | ")
        # remove empty elements in list
        card_numbers = list(filter(None, info[1].split(" ")))
        picked_numbers = list(filter(None, info[0].split(" ")))
        current_score = 0
        for number in card_numbers:
            if number in picked_numbers:
                if current_score == 0:
                    current_score = 1
                else:
                    current_score *= 2
        total += current_score
    
    return total


from functools import cache

def part2(input):
    scores = [0 for _ in range(len(input))]

    for card in input:
        info = card.split(": ")
        card_num = int(info[0].removeprefix("Card ").strip())
        info = info[1].split(" | ")
        # remove empty elements in list
        card_numbers = list(filter(None, info[1].split(" ")))
        picked_numbers = list(filter(None, info[0].split(" ")))
        score = 0
        for number in card_numbers:
            if number in picked_numbers:
                score += 1
        scores[card_num - 1] = score

    @cache
    def calculate_card(idx, depth=0):
        if idx >= len(scores):
            return 0
        score = scores[idx]
        if score == 0:
            return 1
        res = 1
        for i in range(score):
            res += calculate_card(idx + i + 1, depth+1)
        return res
    
    return sum(calculate_card(i) for i in range(len(scores)))

print("Total score: ", part1(data))
print("Totals: ", part2(data))