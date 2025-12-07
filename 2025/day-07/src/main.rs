use std::{collections::HashMap, fs};

fn main() {
    let input = fs::read_to_string("./input.txt").expect("input.txt not found!");

    let (part1, part2) = solve(input);

    println!("Part 1 - Manifold Splits: {}", part1);
    println!("Part 2 - Quantum Manifold Timelines: {}", part2);
}

fn add_beam(beams: &mut HashMap<usize, usize>, beam: usize, num: &usize) {
    let beam_pos = beams.get_mut(&beam);

    if beam_pos.is_none() {
        beams.insert(beam, num.clone());
    } else {
        (*beam_pos.unwrap()) += num;
    }
}

fn solve(input: String) -> (usize, usize) {
    let important_lines: Vec<&str> = input
        .lines()
        .enumerate()
        .filter(|(i, _)| i % 2 == 0)
        .map(|val| val.1)
        .collect();

    let mut beams: HashMap<usize, usize> = HashMap::new();
    beams.insert(important_lines[0].find('S').unwrap(), 1);
    let mut splits = 0;

    important_lines.iter().skip(1).for_each(|line| {
        let str_bytes = line.as_bytes();
        let mut new_beams = HashMap::new();
        for beam in beams.iter() {
            if str_bytes[*beam.0] == b'^' {
                if beam.0 > &0 {
                    add_beam(&mut new_beams, beam.0 - 1, beam.1);
                }
                if beam.0 < &str_bytes.len() {
                    add_beam(&mut new_beams, beam.0 + 1, beam.1);
                }
                splits += 1;
            } else {
                add_beam(&mut new_beams, beam.0.clone(), beam.1);
            }
        }
        beams = new_beams;
    });

    (splits, beams.iter().map(|val| val.1.clone()).sum())
}
