# load input.txt
with open("input.txt", "r") as f:
    input_raw = f.read().splitlines()


# part 1
def part1(input):
    condition = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    # parse and validate the game input
    valid_games = []

    for i, game in enumerate(input):
        id = int(i) + 1
        game_data = game.split(": ")[1]
        round_data = game_data.split("; ")
        is_valid = True
        for data in round_data:
            for pull_data in data.split(", "):
                pull = pull_data.split(" ")
                if int(pull[0]) > condition[pull[1]]:
                    is_valid = False
                    break
        if not is_valid:
            continue

        valid_games.append(id)

    return sum(valid_games)


def part2(input):
    power_sums = 0

    for game in input:
        game_data = game.split(": ")[1]
        round_data = game_data.split("; ")
        highest_pulls = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for data in round_data:
            for pull_data in data.split(", "):
                pull = pull_data.split(" ")
                highest_pulls[pull[1]] = max(highest_pulls[pull[1]], int(pull[0]))

        # multiply the highest pulls together
        power_sums += (
            highest_pulls["red"] * highest_pulls["green"] * highest_pulls["blue"]
        )

    return power_sums


print("(Part 1) Sum of Valid Game Ids: " + str(part1(input_raw)))
print("(Part 2) Sum of Power Levels: " + str(part2(input_raw)))
