use std::fs;

#[derive(Clone, PartialEq)]
enum TileType {
    Robot,
    Box,
    Wall,
    Empty,
}

#[derive(Clone, PartialEq)]
enum Dir {
    Up,
    Right,
    Down,
    Left,
}

fn get_robot_position(map: &Vec<Vec<TileType>>) -> (usize, usize) {
    for (y, row) in map.iter().enumerate() {
        for (x, tile) in row.iter().enumerate() {
            if *tile == TileType::Robot {
                return (x, y);
            }
        }
    }
    panic!("No robot in map!");
}

fn get_in_dir(pos: (usize, usize), dir: &Dir, swap: bool) -> (usize, usize) {
    match dir {
        Dir::Up => (pos.0, (pos.1 as isize - if swap { -1 } else { 1 }) as usize),
        Dir::Right => ((pos.0 as isize + if swap { -1 } else { 1 }) as usize, pos.1),
        Dir::Down => (pos.0, (pos.1 as isize + if swap { -1 } else { 1 }) as usize),
        Dir::Left => ((pos.0 as isize - if swap { -1 } else { 1 }) as usize, pos.1),
    }
}

fn move_robot(
    map: &mut Vec<Vec<TileType>>,
    dir: &Dir,
    current_update_pos: (usize, usize),
) -> Result<(), ()> {
    let tile_at_pos = map[current_update_pos.1][current_update_pos.0].clone();

    if tile_at_pos == TileType::Wall {
        return Err(());
    } else if tile_at_pos == TileType::Robot {
        let result = move_robot(map, dir, get_in_dir(current_update_pos, dir, false));
        if result.is_err() {
            return result;
        } else {
            map[current_update_pos.1][current_update_pos.0] = TileType::Empty;
        }
    } else {
        if tile_at_pos == TileType::Box {
            let result = move_robot(map, dir, get_in_dir(current_update_pos, dir, false));
            if result.is_err() {
                return result;
            }
        }

        let old = get_in_dir(current_update_pos, dir, true);
        map[current_update_pos.1][current_update_pos.0] = map[old.1][old.0].clone();
    }

    return Ok(());
}

fn calculate_gps_score(map: &Vec<Vec<TileType>>) -> u64 {
    let mut total = 0;
    for (y, row) in map.iter().enumerate() {
        for (x, tile) in row.iter().enumerate() {
            if *tile == TileType::Box {
                total += 100 * y as u64 + x as u64;
            }
        }
    }
    total
}

fn part1(orig_map: &Vec<Vec<TileType>>, steps: &Vec<Dir>) -> u64 {
    let mut map = orig_map.clone();

    for direction in steps {
        let robot_pos = get_robot_position(&map);
        let _ = move_robot(&mut map, direction, robot_pos);
    }

    for row in map.iter() {
        for tile in row {
            match tile {
                TileType::Box => print!("O"),
                TileType::Wall => print!("#"),
                TileType::Empty => print!("."),
                TileType::Robot => print!("@"),
            }
        }
        println!();
    }

    calculate_gps_score(&map)
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let data_parts = contents.split("\n\n").collect::<Vec<&str>>();

    let map = data_parts[0]
        .split("\n")
        .map(|map_line| {
            map_line
                .chars()
                .map(|tile| match tile {
                    '#' => TileType::Wall,
                    'O' => TileType::Box,
                    '.' => TileType::Empty,
                    '@' => TileType::Robot,
                    _ => panic!("Invalid Puzzle Input"),
                })
                .collect::<Vec<TileType>>()
        })
        .collect::<Vec<Vec<TileType>>>();

    let actions = data_parts[1]
        .chars()
        .filter(|val| *val != '\n')
        .map(|direction| match direction {
            '^' => Dir::Up,
            '>' => Dir::Right,
            'v' => Dir::Down,
            '<' => Dir::Left,
            _ => panic!("Invalid Puzzle Input: {}", direction),
        })
        .collect::<Vec<Dir>>();

    println!("Total GPS Coordinates (Part 1): {}", part1(&map, &actions));
}
