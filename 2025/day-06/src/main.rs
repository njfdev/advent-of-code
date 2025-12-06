use std::fs;

fn main() {
    let input = fs::read_to_string("./input.txt").expect("input.txt not found!");

    println!("Part 1 - Grand Math Total: {}", part1(input.clone()));
    println!(
        "Part 2 - Correct Grand Math Total: {}",
        part2(input.clone())
    );
}

fn preprocess_input(input: String) -> Vec<(Vec<usize>, char)> {
    let mut nums: Vec<Vec<usize>> = vec![];
    let mut operators: Vec<char> = vec![];

    let lines = input.lines();
    let length = lines.clone().count();

    lines.enumerate().for_each(|(index, line)| {
        if index == length - 1 {
            operators = line
                .split_whitespace()
                .map(|val| val.chars().nth(0).unwrap())
                .collect();
        } else {
            nums.push(
                line.split_whitespace()
                    .map(|val| val.parse::<usize>().unwrap())
                    .collect(),
            );
        }
    });

    operators
        .iter()
        .enumerate()
        .map(|(i, operator)| (nums.iter().map(|nums| nums[i]).collect(), *operator))
        .collect()
}

fn part1(input: String) -> usize {
    let data = preprocess_input(input);

    data.iter()
        .map(|problem| -> usize {
            return if problem.1 == '*' {
                (*problem).0.iter().product()
            } else {
                (*problem).0.iter().sum()
            };
        })
        .sum()
}

fn part2(input: String) -> usize {
    let lines: Vec<&str> = input.lines().collect();
    let operators_split = lines.last().unwrap().split(" ");
    let mut operators: Vec<(char, usize)> = vec![];

    operators_split.for_each(|vals| {
        if vals.len() == 0 {
            operators.last_mut().unwrap().1 += 1;
        } else {
            operators.push((vals.chars().nth(0).unwrap(), 2));
        }
    });

    let mut nums: Vec<Vec<usize>> = vec![vec![0; operators[0].1 - 1]];
    let mut i = 0;
    let mut end = operators[0].1;

    for x in 0..lines[0].len() {
        if (x >= end) {
            i += 1;
            end += operators[i].1;
            nums.push(vec![0; operators[i].1 - 1]);
        }

        let num_index = x - (end - operators[i].1);

        for y in 0..(lines.len() - 1) {
            let line = lines[y].chars();
            let char = line.clone().nth(x).unwrap();
            if char == ' ' {
                continue;
            }
            nums[i][num_index] *= 10;
            nums[i][num_index] += char.to_digit(10).unwrap() as usize;
        }
    }

    operators
        .iter()
        .enumerate()
        .map(|(i, operator_data)| -> usize {
            return if operator_data.0 == '*' {
                nums[i].iter().product()
            } else {
                nums[i].iter().sum()
            };
        })
        .sum()
}
