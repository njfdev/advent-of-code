use std::fs;

use regex::Regex;

fn part1(memory: &String) -> u64 {
    let re = Regex::new(r"mul\([0-9]+,[0-9]+\)").unwrap();

    let matches = re.find_iter(&memory).map(|val| val.as_str());

    let mut total = 0;

    for command in matches {
        let parts: Vec<&str> = command.split(",").collect();

        let num1 = parts[0]
            .strip_prefix("mul(")
            .unwrap()
            .parse::<u64>()
            .unwrap();
        let num2 = parts[1].strip_suffix(")").unwrap().parse::<u64>().unwrap();

        total += num1 * num2;
    }

    return total;
}

fn part2(memory: &String) -> u64 {
    let re = Regex::new(r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)").unwrap();

    let matches = re.find_iter(&memory).map(|val| val.as_str());

    let mut total = 0;
    let mut is_enabled = true;
    for command in matches {
        if command == "do()" {
            is_enabled = true;
        } else if command == "don't()" {
            is_enabled = false;
        } else if is_enabled {
            let parts: Vec<&str> = command.split(",").collect();

            let num1 = parts[0]
                .strip_prefix("mul(")
                .unwrap()
                .parse::<u64>()
                .unwrap();
            let num2 = parts[1].strip_suffix(")").unwrap().parse::<u64>().unwrap();

            total += num1 * num2;
        }
    }

    return total;
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    println!("Total Multiplication Value (Part 1): {}", part1(&contents));
    println!("Total Multiplication Value (Part 2): {}", part2(&contents));
}
