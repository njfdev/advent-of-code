use std::fs;

fn find_good(data: &Vec<(u64, Vec<u64>)>, use_concat: bool) -> u64 {
    let mut total = 0;

    for equation in data {
        let mut possible: Vec<u64> = vec![equation.1[0]];
        for part in equation.1[1..].iter() {
            let mut new_possible: Vec<u64> = vec![];
            for possible_val in possible.clone() {
                new_possible.push(possible_val + part);
                new_possible.push(possible_val * part);
                if use_concat {
                    new_possible.push(
                        (possible_val.to_string() + &part.to_string())
                            .parse::<u64>()
                            .unwrap(),
                    );
                }
            }
            possible = new_possible;
        }

        for possible_val in possible {
            if possible_val == equation.0 {
                total += possible_val;
                break;
            }
        }
    }

    total
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let lines = contents
        .split("\n")
        .map(|str| str.to_string())
        .collect::<Vec<String>>();

    let data_strs = lines
        .iter()
        .map(|val| val.split(": ").collect::<Vec<&str>>())
        .collect::<Vec<Vec<&str>>>();

    let data: Vec<(u64, Vec<u64>)> = data_strs
        .iter()
        .map(|val| {
            (
                val[0].parse::<u64>().unwrap(),
                val[1]
                    .split(" ")
                    .map(|val| val.parse::<u64>().unwrap())
                    .collect(),
            )
        })
        .collect();

    println!(
        "Total Calibration Result (Part 1): {}",
        find_good(&data, false)
    );
    println!(
        "Total Calibration Result (Part 2): {}",
        find_good(&data, true)
    );
}
