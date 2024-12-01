use std::fs;

fn get_min_index(arr: &Vec<i64>) -> usize {
    let mut min_index = 0;
    for (i, val) in arr.iter().enumerate() {
        if *val > arr[min_index] {
            min_index = i;
        }
    }
    return min_index;
}

// TODO: could be optimized by first sorting the vec, then adding corresponding values in each
fn part1(orig_list1: &Vec<i64>, orig_list2: &Vec<i64>) -> i64 {
    let mut list1 = orig_list1.clone();
    let mut list2 = orig_list2.clone();

    let mut total_dist = 0;

    while list1.len() > 0 || list2.len() > 0 {
        let list1_min_index = get_min_index(&list1);
        let list2_min_index = get_min_index(&list2);

        total_dist += (list1[list1_min_index] - list2[list2_min_index]).abs();

        list1.remove(list1_min_index);
        list2.remove(list2_min_index);
    }

    return total_dist;
}

// TODO: could be optimized by storing already found similarity values in a LUT
fn part2(list1: &Vec<i64>, list2: &Vec<i64>) -> i64 {
    let mut similarity_score = 0;

    for list1_val in list1.iter() {
        let mut total_same = 0;
        for list2_val in list2.iter() {
            if list1_val == list2_val {
                total_same += 1;
            }
        }
        similarity_score += list1_val * total_same;
    }

    return similarity_score;
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let mut list1: Vec<i64> = vec![];
    let mut list2: Vec<i64> = vec![];

    for line in contents.lines() {
        let list_values: Vec<&str> = line.split_ascii_whitespace().collect();
        list1.push(
            list_values[0]
                .parse::<i64>()
                .expect("First column should be a number"),
        );
        list2.push(
            list_values[1]
                .parse::<i64>()
                .expect("Second column should be a number"),
        );
    }

    println!("Total Distance (Part 1): {}", part1(&list1, &list2));
    println!("Similarity Score (Part 2): {}", part2(&list1, &list2));
}
