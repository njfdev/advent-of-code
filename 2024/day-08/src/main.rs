use std::{collections::HashSet, fs};

#[derive(Debug, Clone)]
struct Station {
    freq: String,
    location: (i64, i64),
}

impl Station {
    pub fn new(freq: String, location: (i64, i64)) -> Self {
        Self { freq, location }
    }
}

fn is_outside_edge(point: (i64, i64), board_dimensions: (i64, i64)) -> bool {
    (point.0 < 0 || point.0 >= board_dimensions.0) || (point.1 < 0 || point.1 >= board_dimensions.1)
}

fn get_antinodes(
    stations: Vec<Station>,
    board_dimensions: (i64, i64),
    harmonics: bool,
) -> Vec<(i64, i64)> {
    let mut antinodes: Vec<(i64, i64)> = vec![];
    if harmonics {
        for station in stations.clone() {
            antinodes.push(station.location.clone());
        }
    }

    for (index, station_a) in stations[0..stations.len() - 1].iter().enumerate() {
        for station_b in stations[index + 1..].iter() {
            let slope_x = station_a.location.0 - station_b.location.0;
            let slope_y = station_a.location.1 - station_b.location.1;

            let mut next_pos_point = (
                slope_x + station_a.location.0,
                slope_y + station_a.location.1,
            );
            while !is_outside_edge(next_pos_point, board_dimensions) {
                antinodes.push(next_pos_point);
                if !harmonics {
                    break;
                }
                next_pos_point.0 += slope_x;
                next_pos_point.1 += slope_y;
            }

            let mut next_neg_point = (
                station_b.location.0 - slope_x,
                station_b.location.1 - slope_y,
            );
            while !is_outside_edge(next_neg_point, board_dimensions) {
                antinodes.push(next_neg_point);
                if !harmonics {
                    break;
                }
                next_neg_point.0 -= slope_x;
                next_neg_point.1 -= slope_y;
            }
        }
    }

    antinodes
        .iter()
        .filter(|val| !is_outside_edge(**val, board_dimensions))
        .map(|val| *val)
        .collect()
}

fn calc_antinodes(data: &Vec<Vec<&str>>, harmonics: bool) -> u64 {
    // find the stations
    let mut stations: Vec<Station> = vec![];
    for (y, row) in data.iter().enumerate() {
        for (x, freq) in row.iter().enumerate() {
            if *freq != "." {
                stations.push(Station::new(freq.to_string(), (x as i64, y as i64)));
            }
        }
    }

    stations.sort_by(|a, b| a.freq.partial_cmp(&b.freq).unwrap());

    // handle matching stations
    let mut antinodes: Vec<(i64, i64)> = vec![];

    let mut current = 0;
    while current < stations.len() {
        let mut matching_stations = vec![stations[current].clone()];
        current += 1;

        while current < stations.len() && stations[current].freq == matching_stations[0].freq {
            matching_stations.push(stations[current].clone());
            current += 1;
        }

        antinodes.extend(get_antinodes(
            matching_stations,
            (data[0].len() as i64, data.len() as i64),
            harmonics,
        ));
    }

    antinodes.drain(..).collect::<HashSet<(i64, i64)>>().len() as u64
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
                .collect::<Vec<&str>>()
        })
        .collect::<Vec<Vec<&str>>>();

    println!(
        "Unique Antinodes (Part 1): {}",
        calc_antinodes(&data, false)
    );
    println!("Unique Antinodes (Part 2): {}", calc_antinodes(&data, true));
}
