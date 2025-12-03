use std::{fs, ops::Range};

fn main() {
    let input = fs::read_to_string("./input.txt").expect("input.txt not found!");

    println!(
        "Part 1 - Best Output Joltage w/ 2 Batteries: {}",
        solve(input.clone(), 2)
    );
    println!(
        "Part 2 - Best Output Joltage w/ 12 Batteries: {}",
        solve(input.clone(), 12)
    );
}

fn get_biggest_leading_number(chunk: &str, range: Range<usize>) -> (usize, u64) {
    let mut biggest: u64 = 0;
    let mut index: usize = 0;
    for i in range {
        let cur = chunk.chars().nth(i as usize).unwrap().to_digit(10).unwrap() as u64;

        if cur > biggest {
            biggest = cur;
            index = i;
        }

        if biggest == 9 {
            break;
        }
    }

    (index, biggest)
}

fn get_max_joltage(bank: &str, num_batteries: usize) -> u64 {
    let mut joltage_vals: Vec<(usize, u64)> = vec![];

    for i in 0..num_batteries {
        let start_search = if i > 0 { joltage_vals[i - 1].0 + 1 } else { 0 };
        let end_search = bank.len() - (num_batteries - 1 - i);
        joltage_vals.push(get_biggest_leading_number(bank, start_search..end_search));
    }

    let joltage = joltage_vals
        .iter()
        .enumerate()
        .map(|(pos, joltage)| joltage.1 * 10_u64.pow(((num_batteries - 1) - pos) as u32))
        .sum();

    joltage
}

fn solve(input: String, num_batteries: usize) -> u64 {
    let joltage_lines = input.lines();

    joltage_lines
        .map(|bank| get_max_joltage(bank, num_batteries))
        .sum()
}
