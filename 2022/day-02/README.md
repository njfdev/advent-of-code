# Day 2 - Advent of Code

You can find the link for day 2, 2022 [here](https://adventofcode.com/2022/day/2). This folder will provide complete solutions for part 1 and part 2 of day 2. I highly recommend trying to solve these problems yourself instead of just copying my code (you will learn a lot more).

This file will explain what the problem is and how to run the code. Explanation of the code will be in comments within the code itself (lines that start with `#`).

## Setup

To run this code, you should get the input from [this link](https://adventofcode.com/2022/day/2/input) and paste it into `game-data.txt` but my input is already provided as a sample. You should also make sure to have Python installed (I use Python 3.10.7 but it should work with most versions).

## Part 1

In part one we have a list of rock, paper, scissors games such as the following:

```
A Y
B X
C Z
```

The first column is the opponents choice and the second is ours.

**Opponent: A = Rock, B = Paper, C = Scissors**

**Us: X = Rock, Y = Paper, Z = Scissors**

If we win the game, we get 6 points. If we tie the game, we get 3 points. If we lose the game, we get 0 points.

If we choose rock, we get 1 point. If we choose paper, we get 2 points. If we choose scissors, we get 3 points.

We must then add all of these together for our answer.

### Run the Code

You can run this command after making sure to follow the [setup](#setup).

```bash
python3 ./part-1-rock-paper-scissors.py
```

## Part 2

We have the same setup as in [part 1](#part-1) and use the same game-data.txt file found in [setup](#setup). This time the last column actually means wether the game won, tied, or lost:
X = Lose
Y = Draw
Z = Win

We use the same scoring from before, but we have to find what our choice is based on the opponents choice and the outcome.

### Run the Code

```bash
python3 ./part-2-rock-paper-scissors.py
```
