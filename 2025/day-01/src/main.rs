use std::fs;

fn main() {
    let input = fs::read_to_string("./input.txt")
        .expect("input.txt doesn't exist in the current directory!");

    println!("Part 1 - Password: {}", solve(input.clone(), false));
    println!("Part 2 - Actual Password: {}", solve(input.clone(), true));
}

fn solve(document: String, part2: bool) -> usize {
    let rotations = document.split("\n");

    let mut cur_num = 50;
    let mut total_zeros = 0;

    rotations.for_each(|rotation| {
        let dir = if rotation.starts_with("L") { -1 } else { 1 };
        let num = rotation[1..].parse::<i32>().unwrap();

        let new_num = cur_num + dir * num;
        let new_wrapped_num = (new_num % 100 + 100) % 100;

        if part2 {
            total_zeros += (new_num.abs() as f32 / 100.0).floor() as usize;
            if new_num <= 0 && cur_num > 0 {
                total_zeros += 1;
            }
        } else if new_wrapped_num == 0 {
            total_zeros += 1;
        }

        cur_num = new_wrapped_num;
    });

    total_zeros
}
