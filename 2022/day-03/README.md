# Day 3 - Advent of Code

You can find the link for day 3, 2022 [here](https://adventofcode.com/2022/day/3). This folder will provide complete solutions for part 1 and part 2 of day 3. I highly recommend trying to solve these problems yourself instead of just copying my code (you will learn a lot more).

This file will explain what the problem is and how to run the code. Explanation of the code will be in comments within the code itself (lines that start with `#`).

## Setup

To run this code, you should get the input from [this link](https://adventofcode.com/2022/day/3/input) and paste it into `rucksack-data.txt` but my input is already provided as a sample. You should also make sure to have Python installed (I use Python 3.10.7 but it should work with most versions).

## Part 1

In part one we have a list strings like the following:

```
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
```

Each string needs to be split in 2 and we need to find which letter is common between both sides. We then have to sum up the priority of the common letter using the scoring below:

- a-z: 1-26
- A-Z: 27-52

### Run the Code

You can run this command after making sure to follow the [setup](#setup).

```bash
python3 ./part-1-rucksack-reorganization.py
```

## Part 2

We have the same setup as in [part 1](#part-1) and use the same rucksack-data.txt file found in [setup](#setup). This time every 3 strings is a group and we need to find the common letter in the group. We sum up all the common letters and calculate the priority using the scoring from above.

### Run the Code

```bash
python3 ./part-2-rucksack-reorganization.py
```
