# read game-data.txt as a newline separated list
with open("game-data.txt") as f:
    raw_games = f.read().splitlines()

# the raw_games is a list of strings with 2 letters
# separated by a space. We need to split each string
# into a list of 2 letters
games = [game.split(" ") for game in raw_games]

# create score variable set at 0
score = 0

# loop through each game
for game in games:
    # this game is rock paper scissors
    # our opponents choice is at index 0 using ABC (rock, paper, scissors)
    # the outcome of the game is at index 1 using XYZ (lose, draw, win)
    # rock beats scissors
    # paper beats rock
    # scissors beats paper
    #
    # We need to find out our choice based on the outcome
    # and assign it to a variable. We get 1 point added to our score
    # for rock, 2 points for paper, and 3 points for scissors.
    # We then add the points to our score
    #
    # After that, we need to calculate the score based on the game result
    # if we win, we get 6 points
    # if we draw, we get 3 points
    # if we lose, we get 0 points
    # We then add the points to our score
    #
    # Truth table:
    # Top is opponent, left is us
    # w=win, d=draw, l=lose
    #   A   B   C
    # A T   W   L
    # B L   T   W
    # C W   L   T
    our_choice = ""

    if game[0] == "A" and game[1] == "X":
        our_choice = "C"
    elif game[0] == "A" and game[1] == "Y":
        our_choice = "A"
    elif game[0] == "A" and game[1] == "Z":
        our_choice = "B"
    elif game[0] == "B" and game[1] == "X":
        our_choice = "A"
    elif game[0] == "B" and game[1] == "Y":
        our_choice = "B"
    elif game[0] == "B" and game[1] == "Z":
        our_choice = "C"
    elif game[0] == "C" and game[1] == "X":
        our_choice = "B"
    elif game[0] == "C" and game[1] == "Y":
        our_choice = "C"
    elif game[0] == "C" and game[1] == "Z":
        our_choice = "A"

    if our_choice == "A":
        score += 1
    elif our_choice == "B":
        score += 2
    elif our_choice == "C":
        score += 3

    if game[1] == "X":
        score += 0
    elif game[1] == "Y":
        score += 3
    elif game[1] == "Z":
        score += 6

# print our score
print("Score:", score)
