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

fn does_2d_match(correct: &String, found: Vec<String>) -> bool {
    // get diagonals
    let down_right = found
        .clone()
        .iter()
        .enumerate()
        .map(|(i, val)| val.get(i..(i + 1)).unwrap())
        .collect::<String>();

    let down_left = found
        .clone()
        .iter()
        .enumerate()
        .map(|(i, val)| val.get((val.len() - i - 1)..(val.len() - i)).unwrap())
        .collect::<String>();

    return (correct == &down_right || correct == &(down_right.chars().rev().collect::<String>()))
        && (correct == &down_left || correct == &(down_left.chars().rev().collect::<String>()));
}

fn part2(wordsearch: &Vec<String>, word: &String) -> u64 {
    let mut total = 0;

    // find all groups of 3
    for r in 0..(wordsearch.len() - word.len() + 1) {
        for c in 0..(wordsearch[r].len() - word.len() + 1) {
            let mut section: Vec<String> = vec![];

            for i in 0..word.len() {
                section.push(wordsearch[r + i][(c)..(c + word.len())].to_string());
            }

            if does_2d_match(&word, section) {
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
    println!(
        "Total X-MASs (Part 2): {}",
        part2(&lines, &("MAS".to_string()))
    );
}
