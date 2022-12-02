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
    # depending on our choice (index of 1), we get a certain amount of points
    # if we choose "X" we get 1 point
    # if we choose "Y" we get 2 points
    # if we choose "Z" we get 3 points
    # we then add the points to our score
    if game[1] == "X":
        score += 1
    elif game[1] == "Y":
        score += 2
    elif game[1] == "Z":
        score += 3

    # now we need to calculate the score based on the game result
    # if we win, we get 6 points
    # if we draw, we get 3 points
    # if we lose, we get 0 points
    #
    # It is just a normal game of rock paper scissors
    # Our opponents choice is at index 0 using ABC (rock, paper, scissors)
    # Our choice is at index 1 using XYZ (rock, paper, scissors)
    # rock beats scissors
    # paper beats rock
    # scissors beats paper
    #
    # Truth table:
    # Top is opponent, left is us
    #   A   B   C
    # X 3   6   0
    # Y 0   3   6
    # Z 6   0   3
    if game[0] == "A" and game[1] == "X":
        score += 3
    elif game[0] == "A" and game[1] == "Y":
        score += 6
    elif game[0] == "A" and game[1] == "Z":
        score += 0
    elif game[0] == "B" and game[1] == "X":
        score += 0
    elif game[0] == "B" and game[1] == "Y":
        score += 3
    elif game[0] == "B" and game[1] == "Z":
        score += 6
    elif game[0] == "C" and game[1] == "X":
        score += 6
    elif game[0] == "C" and game[1] == "Y":
        score += 0
    elif game[0] == "C" and game[1] == "Z":
        score += 3


# print our score
print("Score:", score)
