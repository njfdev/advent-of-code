use std::{fs, ops::Range, process::id};

fn main() {
    let input = fs::read_to_string("./input.txt").expect("input.txt not found!");

    let mut split_input = input.split("\n\n");
    let mut ranges: Vec<Range<usize>> = split_input
        .next()
        .unwrap()
        .split("\n")
        .map(|range_str| {
            let nums: Vec<usize> = range_str
                .split("-")
                .map(|val| val.parse::<usize>().unwrap())
                .collect();
            nums[0]..(nums[1] + 1)
        })
        .collect();
    ranges = condense_ranges(&ranges);

    let ids: Vec<usize> = split_input
        .next()
        .unwrap()
        .split("\n")
        .map(|val| val.parse::<usize>().unwrap())
        .collect();

    println!(
        "Part 1 - # of Fresh Ingredient IDs: {}",
        part1(&ranges, &ids)
    );

    println!("Part 2 - Total Fresh Ingredient IDs: {}", part2(&ranges));
}

fn is_in_ranges(num: usize, ranges: &Vec<Range<usize>>) -> bool {
    for range in ranges {
        if range.contains(&num) {
            return true;
        }
    }
    return false;
}

fn condense_ranges(old_ranges: &Vec<Range<usize>>) -> Vec<Range<usize>> {
    let mut ranges = old_ranges.clone();
    let mut i: isize = 0;
    while i < (ranges.len() - 1) as isize {
        let mut j: isize = i + 1;
        while j < ranges.len() as isize {
            let starti_after_startj = ranges[i as usize].start >= ranges[j as usize].start;
            let starti_before_endj = ranges[i as usize].start < ranges[j as usize].end;
            let endi_before_endj = ranges[i as usize].end <= ranges[j as usize].end;
            let endi_after_startj = ranges[i as usize].end > ranges[j as usize].start;

            let start_is_between = starti_after_startj && starti_before_endj;
            let end_is_less = endi_before_endj && endi_after_startj;

            if start_is_between && !end_is_less {
                ranges[j as usize] = ranges[j as usize].start..ranges[i as usize].end;
            } else if !start_is_between && end_is_less {
                ranges[j as usize] = ranges[i as usize].start..ranges[j as usize].end;
            }

            if start_is_between || end_is_less {
                ranges.remove(i as usize);
                i -= 1;
                j -= 1;
                break;
            } else if (starti_before_endj && endi_after_startj) {
                ranges.remove(j as usize);
            }
            j += 1;
        }
        i += 1;
    }
    ranges
}

fn part1(ranges: &Vec<Range<usize>>, ids: &Vec<usize>) -> usize {
    let mut total_ids = 0;

    ids.iter().for_each(|id| {
        if is_in_ranges(*id, ranges) {
            total_ids += 1;
        }
    });

    total_ids
}

fn part2(ranges: &Vec<Range<usize>>) -> usize {
    ranges
        .iter()
        .map(|range| {
            let val = range.end - range.start;
            val
        })
        .sum()
}
