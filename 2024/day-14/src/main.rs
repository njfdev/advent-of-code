use std::fs;

const MAP_WIDTH: usize = 101;
const MAP_HEIGHT: usize = 103;

#[derive(Clone, Debug)]
struct Robot {
    pos: (usize, usize),
    vel: (isize, isize),
}

fn update_robot_pos(robot: &mut Robot) {
    robot.pos.0 = ((robot.vel.0 + robot.pos.0 as isize).rem_euclid(MAP_WIDTH as isize)) as usize;
    robot.pos.1 = ((robot.vel.1 + robot.pos.1 as isize).rem_euclid(MAP_HEIGHT as isize)) as usize;
}

fn is_next_to_another_robot(robots: &Vec<Robot>, robot: &Robot) -> bool {
    for pos_robot in robots {
        if pos_robot.pos.0 == robot.pos.0 && pos_robot.pos.1 == robot.pos.1 {
            continue;
        }

        if (pos_robot.pos.0 as isize - robot.pos.0 as isize).abs() <= 1
            && (pos_robot.pos.1 as isize - robot.pos.1 as isize).abs() <= 1
        {
            return true;
        }
    }

    false
}

fn print_grid(robots: &Vec<Robot>) {
    for y in 0..MAP_HEIGHT {
        for x in 0..MAP_WIDTH {
            let mut total = 0;
            for robot in robots {
                if robot.pos.0 == x && robot.pos.1 == y {
                    total += 1;
                }
            }

            if total == 0 {
                print!(".");
            } else {
                print!("{}", total);
            }
        }
        println!();
    }
}

fn calc_sf_score(robots_orig: &Vec<Robot>) -> u64 {
    let mut quadrants: [u64; 4] = [0, 0, 0, 0];
    for robot in robots_orig {
        // quadrant 1
        if robot.pos.0 < MAP_WIDTH / 2 && robot.pos.1 < MAP_HEIGHT / 2 {
            quadrants[0] += 1;
        // quadrant 2
        } else if robot.pos.0 > MAP_WIDTH / 2 && robot.pos.1 < MAP_HEIGHT / 2 {
            quadrants[1] += 1;
        // quadrant 3
        } else if robot.pos.0 < MAP_WIDTH / 2 && robot.pos.1 > MAP_HEIGHT / 2 {
            quadrants[2] += 1;
        // quadrant 4
        } else if robot.pos.0 > MAP_WIDTH / 2 && robot.pos.1 > MAP_HEIGHT / 2 {
            quadrants[3] += 1;
        }
    }
    quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
}

fn calc_sf_at_time(robots_orig: &Vec<Robot>, iterations: u32, max: u32) -> u64 {
    let mut robots = robots_orig.clone();

    let mut lowest_safety_factor_map = robots.clone();
    let mut lowest_safety_factor = calc_sf_score(&robots);
    let mut lowest_safety_factor_id = 0;

    let mut final_safety_score = 0;

    for i in 0..max {
        if i == 100 {
            final_safety_score = calc_sf_score(&robots);
        }

        for robot in robots.iter_mut() {
            update_robot_pos(robot);
        }

        let new_sf = calc_sf_score(&robots);
        if new_sf < lowest_safety_factor {
            lowest_safety_factor_map = robots.clone();
            lowest_safety_factor = new_sf;
            lowest_safety_factor_id = i;
        }
    }

    print_grid(&lowest_safety_factor_map);
    println!(
        "Christmas Tree Iteration (Part 2): {}\n",
        lowest_safety_factor_id + 1
    );

    final_safety_score
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let robots_nums = contents
        .split("\n")
        .map(|robot_str| {
            let parts = robot_str
                .split(" ")
                .map(|val| {
                    val.split("=").collect::<Vec<&str>>()[1]
                        .split(",")
                        .map(|num| num.parse::<isize>().unwrap())
                        .collect::<Vec<isize>>()
                })
                .collect();
            parts
        })
        .collect::<Vec<Vec<Vec<isize>>>>();

    let robots = robots_nums
        .iter()
        .map(|robot_data| Robot {
            pos: (robot_data[0][0] as usize, robot_data[0][1] as usize),
            vel: (robot_data[1][0], robot_data[1][1]),
        })
        .collect::<Vec<Robot>>();

    println!(
        "Safety Factor (Part 1): {}",
        calc_sf_at_time(&robots, 100, 10000)
    );
}
