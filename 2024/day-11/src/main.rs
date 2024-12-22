use std::fs;

fn stone_index(stones_dict: &mut Vec<(u64, u64)>, stone_num: u64) -> Option<usize> {
    for (i, val) in stones_dict.iter_mut().enumerate() {
        if val.0 == stone_num {
            return Some(i);
        }
    }
    return None;
}

fn update_stones_dict(stones_dict: &mut Vec<(u64, u64)>, stone_num: u64, stone_change: i64) {
    let index = stone_index(stones_dict, stone_num);

    if index.is_some() {
        if stones_dict[index.unwrap()].1 == -stone_change as u64 {
            stones_dict.remove(index.unwrap());
            return;
        }

        stones_dict[index.unwrap()] = (
            stone_num,
            (stones_dict[index.unwrap()].1 as i64 + stone_change) as u64,
        );
    } else {
        stones_dict.push((stone_num, stone_change as u64));
    }
}

fn faster_blink(stones: &Vec<u64>, count: usize) -> u64 {
    // stored as (stone_number, occurrence)
    let mut stones_dict: Vec<(u64, u64)> = vec![];

    for initial_val in stones {
        update_stones_dict(&mut stones_dict, *initial_val, 1);
    }

    for _ in 0..count {
        let mut new_stones_dict = stones_dict.clone();
        for i in 0..stones_dict.len() {
            let stone = stones_dict[i];

            // handle zero stones
            if stone.0 == 0 {
                update_stones_dict(&mut new_stones_dict, 1, stone.1 as i64);
                update_stones_dict(&mut new_stones_dict, 0, -(stone.1 as i64));
                continue;
            }

            let stone_str = &*stone.0.to_string();
            if stone_str.len() % 2 == 0 {
                let new_stone_1 = stone_str[0..stone_str.len() / 2].parse::<u64>().unwrap();
                let new_stone_2 = stone_str[stone_str.len() / 2..].parse::<u64>().unwrap();

                update_stones_dict(&mut new_stones_dict, new_stone_1, stone.1 as i64);
                update_stones_dict(&mut new_stones_dict, new_stone_2, stone.1 as i64);
                update_stones_dict(&mut new_stones_dict, stone.0, -(stone.1 as i64));
            } else {
                update_stones_dict(&mut new_stones_dict, stone.0 * 2024, stone.1 as i64);
                update_stones_dict(&mut new_stones_dict, stone.0, -(stone.1 as i64));
            }
        }
        stones_dict = new_stones_dict;
    }

    stones_dict.iter().map(|(_, count)| count).sum()
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let stones = contents
        .split(" ")
        .map(|str| str.parse::<u64>().unwrap())
        .collect::<Vec<u64>>();

    println!(
        "Stones After 25 Blinks (Part 1): {}",
        faster_blink(&stones, 25)
    );
    println!(
        "Stones After 75 Blinks (Part 2): {}",
        faster_blink(&stones, 75)
    );
}
