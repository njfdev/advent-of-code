use std::fs;

fn get_trailhead_score(
    map: &Vec<Vec<i8>>,
    point: &(usize, usize),
    previous: i8,
    already_found: &mut Option<Vec<(usize, usize)>>,
) -> u64 {
    let cur = map[point.1][point.0].clone();

    if cur != previous + 1
        || (already_found.is_some() && already_found.as_mut().unwrap().contains(point))
    {
        return 0;
    }

    if cur == 9 {
        if already_found.is_some() {
            already_found.as_mut().unwrap().push(point.clone());
        }
        return 1;
    }

    let mut total = 0;

    if point.0 > 0 {
        total += get_trailhead_score(map, &(point.0 - 1, point.1), cur, already_found);
    }
    if point.1 > 0 {
        total += get_trailhead_score(map, &(point.0, point.1 - 1), cur, already_found);
    }
    if point.1 < map.len() - 1 {
        total += get_trailhead_score(map, &(point.0, point.1 + 1), cur, already_found);
    }
    if point.0 < map[0].len() - 1 {
        total += get_trailhead_score(map, &(point.0 + 1, point.1), cur, already_found);
    }

    return total;
}

fn calc_scores(map: &Vec<Vec<i8>>, is_part_2: bool) -> u64 {
    let mut starting_points = vec![];

    for (y, row) in map.iter().enumerate() {
        for (x, height) in row.iter().enumerate() {
            if *height == 0 {
                starting_points.push((x, y));
            }
        }
    }

    starting_points
        .iter()
        .map(|point| {
            let mut tmp = if is_part_2 { None } else { Some(vec![]) };
            get_trailhead_score(map, point, -1, &mut tmp)
        })
        .sum()
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let lines = contents
        .split("\n")
        .map(|str| str.to_string())
        .collect::<Vec<String>>();

    let data = lines
        .iter()
        .map(|val| {
            val.split("")
                .filter(|val| *val != "")
                .map(|val| val.parse::<i8>().unwrap())
                .collect::<Vec<i8>>()
        })
        .collect::<Vec<Vec<i8>>>();

    println!(
        "Total Trailhead Scores (Part 1): {}",
        calc_scores(&data, false)
    );
    println!(
        "Total Trailhead Ratings (Part 2): {}",
        calc_scores(&data, true)
    );
}
