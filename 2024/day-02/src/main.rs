use std::fs;

fn calculate_safe(level: &Vec<i64>) -> bool {
    let direction = if level[1] - level[0] > 0 { 1 } else { -1 };

    let mut is_safe = true;
    for i in 1..level.len() {
        let diff = (level[i] - level[i - 1]) * direction;
        if diff < 1 || diff > 3 {
            is_safe = false;
            continue;
        }
    }

    return is_safe;
}

fn part1(reports: &Vec<Vec<i64>>) -> usize {
    let mut total_safe: usize = 0;

    for level in reports.iter() {
        if calculate_safe(level) {
            total_safe += 1;
        }
    }

    return total_safe;
}

fn part2(reports: &Vec<Vec<i64>>) -> usize {
    let mut total_safe = 0;

    for level in reports.iter() {
        if calculate_safe(level) {
            total_safe += 1;
        } else {
            for i in 0..level.len() {
                let mut removed_level = level.clone();
                removed_level.remove(i);
                if calculate_safe(&removed_level) {
                    total_safe += 1;
                    break;
                }
            }
        }
    }

    return total_safe;
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let mut reports: Vec<Vec<i64>> = vec![];

    for line in contents.lines() {
        reports.push(
            line.trim()
                .split(" ")
                .into_iter()
                .map(|val| val.parse::<i64>().expect("Each value is a number"))
                .collect(),
        );
    }

    println!("Safe Reports (Part 1): {}", part1(&reports));
    println!("Safe Reports (Part 2): {}", part2(&reports));
}
