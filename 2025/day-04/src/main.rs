use std::fs;

fn main() {
    let input = fs::read_to_string("./input.txt").expect("input.txt not found!");

    println!(
        "Part 1 - Accessible Rolls of Paper: {}",
        solve(input.clone(), false)
    );
    println!(
        "Part 2 - Total Accessible Rolls of Paper: {}",
        solve(input.clone(), true)
    );
}

fn get_surrounding_roll_indicies(x: usize, y: usize, map: &Vec<String>) -> Vec<(usize, usize)> {
    let mut accessible = vec![];

    for to_check_y in (y as isize - 1)..=(y as isize + 1) {
        for to_check_x in (x as isize - 1)..=(x as isize + 1) {
            if (to_check_x == x as isize && to_check_y == y as isize)
                || (to_check_y < 0 || to_check_y as usize >= map.len())
                || (to_check_x < 0 || to_check_x as usize >= map[0].len())
            {
                continue;
            }

            let at_pos = map[to_check_y as usize]
                .clone()
                .chars()
                .nth(to_check_x as usize)
                .unwrap();

            if at_pos == '@' {
                accessible.push((to_check_x as usize, to_check_y as usize));
            }
        }
    }

    accessible
}

fn get_is_possible_roll(x: usize, y: usize, map: &Vec<String>) -> bool {
    if map[y].chars().clone().nth(x).unwrap() != '@' {
        return false;
    }

    let possible_rolls = get_surrounding_roll_indicies(x, y, map);

    possible_rolls.len() < 4
}

fn solve(input: String, part2: bool) -> usize {
    let mut map: Vec<String> = input.lines().map(|val| val.to_string()).collect();

    let mut total_rolls = 0;

    let mut last_loop_accessible = 1;
    while (part2 && last_loop_accessible > 0) || total_rolls == 0 {
        last_loop_accessible = 0;
        for y in 0..map[0].len() {
            for x in 0..map.len() {
                let accessible = get_is_possible_roll(x, y, &map);

                if accessible {
                    if part2 {
                        map[y].replace_range(x..(x + 1), ".");
                    }

                    last_loop_accessible += 1;
                }
            }
        }
        total_rolls += last_loop_accessible;
    }

    total_rolls
}
