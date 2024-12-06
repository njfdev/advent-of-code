use std::fs;

#[derive(Debug, PartialEq)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

fn find_guard(grid: &Vec<String>) -> ((i64, i64), Direction) {
    for y in 0..grid.len() {
        for x in 0..grid[y].len() {
            if &grid[y][x..(x + 1)] == "^" {
                return ((x as i64, y as i64), Direction::Up);
            }
        }
    }

    panic!("No guard in input.txt");
}

fn is_point_off_edge(grid: &Vec<String>, point: (i64, i64)) -> bool {
    return point.0 >= grid[0].len() as i64
        || point.0 < 0
        || point.1 >= grid.len() as i64
        || point.1 < 0;
}

fn get_point_in_dir(cur: &(i64, i64), dir: &Direction) -> (i64, i64) {
    match dir {
        Direction::Up => return (cur.0 as i64, cur.1 as i64 - 1),
        Direction::Down => return (cur.0 as i64, cur.1 as i64 + 1),
        Direction::Right => return (cur.0 as i64 + 1, cur.1 as i64),
        Direction::Left => return (cur.0 as i64 - 1, cur.1 as i64),
    }
}

fn move_guard(grid: &mut Vec<String>, guard_details: &mut ((i64, i64), Direction)) {
    let mut next_pos = get_point_in_dir(&guard_details.0, &guard_details.1);

    while &grid[next_pos.1 as usize][next_pos.0 as usize..(next_pos.0 as usize + 1)] == "#" {
        match guard_details.1 {
            Direction::Up => guard_details.1 = Direction::Right,
            Direction::Right => guard_details.1 = Direction::Down,
            Direction::Down => guard_details.1 = Direction::Left,
            Direction::Left => guard_details.1 = Direction::Up,
        }
        next_pos = get_point_in_dir(&guard_details.0, &guard_details.1);
    }

    grid[next_pos.1 as usize].replace_range(next_pos.0 as usize..(next_pos.0 as usize + 1), "X");
    guard_details.0 = next_pos;
}

fn part1(orig_grid: &Vec<String>) -> u64 {
    let mut grid = orig_grid.clone();

    let mut guard_details = find_guard(&grid);

    grid[guard_details.0 .1 as usize].replace_range(
        guard_details.0 .0 as usize..(guard_details.0 .0 as usize + 1),
        "X",
    );

    while !is_point_off_edge(&grid, get_point_in_dir(&guard_details.0, &guard_details.1)) {
        move_guard(&mut grid, &mut guard_details);
    }

    println!("Final Grid:\n{:#?}", grid);

    return grid
        .iter()
        .map(|vec| vec.chars().filter(|c| *c == 'X').count() as u64)
        .sum();
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let lines = contents
        .split("\n")
        .map(|str| str.to_string())
        .collect::<Vec<String>>();

    println!("Distinct Positions (Part 1): {}", part1(&lines));
    // println!(
    //     "Bad Updates Values (Part 2): {}",
    //     handle_updates(&rules, &updates, true)
    // );
}
