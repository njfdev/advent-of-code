use std::fs;

fn main() {
    let input = fs::read_to_string("./input.txt").expect("index.txt doesn't exist!");

    println!("Part 1 - Invalid ID sum: {}", solve(input.clone(), false));
    println!(
        "Part 2 - Actual Invalid ID sum: {}",
        solve(input.clone(), true)
    );
}

fn count_digits(num: usize) -> usize {
    let mut digits = 0;
    let mut cur = num;
    while cur > 0 {
        cur /= 10;
        digits += 1;
    }
    return digits;
}

fn select_digits(num: usize, start: usize, len: usize) -> usize {
    let new_chunk = num / 10_usize.pow(start as u32);
    let upper_chunk = (new_chunk / 10_usize.pow(len as u32)) * 10_usize.pow(len as u32);
    return new_chunk - upper_chunk;
}

fn check_repeat_size(num: usize, digits: usize, repeat_size: usize) -> bool {
    let base = select_digits(num, 0, repeat_size);

    for i in 1..(digits / repeat_size) {
        let cur = select_digits(num, i * repeat_size, repeat_size);
        if cur != base {
            return false;
        }
    }

    return true;
}

fn solve(input: String, part2: bool) -> usize {
    let id_ranges = input.split(",").map(|range| {
        let parts: Vec<usize> = range
            .split("-")
            .map(|val| val.parse::<usize>().unwrap())
            .collect();

        return parts[0]..=parts[1];
    });

    let mut invalid_sum = 0;
    id_ranges.for_each(|range| {
        for num in range {
            let digits = count_digits(num);

            if !part2 && digits % 2 == 0 {
                let shift = 10_usize.pow(digits as u32 / 2);
                let upper_chunk = num / shift;
                let lower_chunk = num - (upper_chunk * shift);

                if upper_chunk == lower_chunk {
                    invalid_sum += num;
                }
            } else {
                for repeat_size in 1..digits {
                    if digits % repeat_size != 0 {
                        continue;
                    }
                    let does_repeat = check_repeat_size(num, digits, repeat_size);

                    if does_repeat {
                        invalid_sum += num;
                        break;
                    }
                }
            }
        }
    });

    invalid_sum
}
