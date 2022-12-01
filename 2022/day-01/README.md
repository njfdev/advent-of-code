# Day 1 - Advent of Code

You can find the link for day 1, 2022 [here](https://adventofcode.com/2022/day/1). This folder will provide complete solutions for part 1 and part 2 of day 1. I highly recommend trying to solve these problems yourself instead of just copying my code (you will learn a lot more).

Thus file will explain what the problem is and how to run the code. Explanation of the code will be in comments within the code itself (lines that start with `#`).

## Setup

To run this code, you should get the input from [this link](https://adventofcode.com/2022/day/1/input) and paste it into `calories.txt` but my input is already provided as a sample. You should also make sure to have Python installed (I use Python 3.10.7 but it should work with most versions).

## Part 1

In part one we have a list of numbers such as the following:

```txt
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
```

Here, we have groups of numbers separated by double newline characters. We have to add up all the numbers in each group like the following:

```txt
6000

4000

11000

24000

10000
```

Now, all we have to do is find the maximum. In this scenario, the maximum would be 24000.

### Run the Code

You can run this command after making sure to follow the [setup](#setup).

```bash
python3 ./part-1-calorie-counting.py
```

## Part 2

We have the same setup as in [part 1](#part-1), but this time we need to find the the top 3 elves and add all of their calories together. You can also use the same calories.txt file found in [setup](#setup).

```bash
python3 ./part-2-calorie-counting.py
```
