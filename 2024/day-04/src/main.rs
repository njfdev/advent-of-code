use std::fs;

fn does_match(correct: &String, found: &String) -> bool {
    return correct == found || correct == &(found.chars().rev().collect::<String>());
}

fn part1(wordsearch: &Vec<String>, word: &String) -> u64 {
    let mut total = 0;

    // find horizontal
    for r in 0..wordsearch.len() {
        for c in 0..(wordsearch[r].len() - word.len() + 1) {
            let section = wordsearch[r][c..(c + word.len())].to_string();
            if does_match(&word, &section) {
                total += 1;
            }
        }
    }

    // find vertical
    for c in 0..wordsearch[0].len() {
        for r in 0..(wordsearch.len() - word.len() + 1) {
            let mut section = wordsearch[r][c..(c + 1)].to_string();

            for i in (r + 1)..(r + word.len()) {
                section += &wordsearch[i][c..(c + 1)];
            }

            if does_match(&word, &section) {
                total += 1;
            }
        }
    }

    // find diagonal down-right
    for r in 0..(wordsearch.len() - word.len() + 1) {
        for c in 0..(wordsearch[r].len() - word.len() + 1) {
            let mut section = wordsearch[r][c..(c + 1)].to_string();

            for i in 1..word.len() {
                section += &wordsearch[r + i][(c + i)..(c + i + 1)];
            }

            if does_match(&word, &section) {
                total += 1;
            }
        }
    }

    // find diagonal down-left
    for r in (word.len() - 1)..wordsearch.len() {
        for c in 0..(wordsearch[r].len() - word.len() + 1) {
            let mut section = wordsearch[r][c..(c + 1)].to_string();

            for i in 1..word.len() {
                section += &wordsearch[r - i][(c + i)..(c + i + 1)];
            }

            if does_match(&word, &section) {
                total += 1;
            }
        }
    }

    return total;
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let lines = contents
        .split("\n")
        .map(|str| str.to_string())
        .collect::<Vec<String>>();

    println!(
        "Total XMASs (Part 1): {}",
        part1(&lines, &("XMAS".to_string()))
    );
    //println!("Total Multiplication Value (Part 2): {}", part2(&contents));
}
