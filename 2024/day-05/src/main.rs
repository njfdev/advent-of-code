use std::fs;

fn get_page_rules(rules: &Vec<(u64, u64)>, num: &u64) -> Vec<(u64, u64)> {
    return rules
        .iter()
        .filter(|rule| rule.0 == num.clone())
        .map(|val| val.clone())
        .collect();
}

fn is_page_in_rules(rules: &Vec<(u64, u64)>, num: &u64) -> bool {
    return rules.iter().any(|val| val.1 == num.clone());
}

fn is_page_valid(update: &Vec<u64>, index: usize, rules: &Vec<(u64, u64)>) -> bool {
    let page_rules = get_page_rules(rules, &update[index]);

    for i in 0..index {
        if is_page_in_rules(&page_rules, &update[i]) {
            return false;
        }
    }

    return true;
}

fn fix_update(update: &Vec<u64>, rules: &Vec<(u64, u64)>) -> Vec<u64> {
    let mut new = update.clone();

    for (cur_index, cur_page) in new.clone()[1..].iter().enumerate() {
        let mut checking_i = cur_index + 1;

        while checking_i > 0 && !is_page_valid(&new, checking_i, rules) {
            checking_i -= 1;
            new[checking_i + 1] = new[checking_i];
            new[checking_i] = cur_page.clone();
        }
    }

    return new;
}

fn handle_updates(rules: &Vec<(u64, u64)>, updates: &Vec<Vec<u64>>, handle_incorrect: bool) -> u64 {
    let mut middle_totals = 0;

    for update in updates.iter() {
        let mut any_invalid = false;
        for (cur_index, cur_page) in update.iter().enumerate() {
            if !is_page_valid(update, cur_index, rules) {
                any_invalid = true;
                break;
            }
        }

        if !any_invalid && !handle_incorrect {
            let middle = update[update.len() / 2];
            middle_totals += middle;
        } else if any_invalid && handle_incorrect {
            let fixed = fix_update(update, rules);
            middle_totals += fixed[fixed.len() / 2];
        }
    }

    return middle_totals;
}

fn main() {
    let contents =
        fs::read_to_string("./src/input.txt").expect("Should be able to read input file");

    let lines = contents
        .split("\n")
        .map(|str| str.to_string())
        .collect::<Vec<String>>();

    let sections = lines
        .split(|val| val == "")
        .map(|val| val.to_owned())
        .collect::<Vec<Vec<String>>>();

    let raw_rules = &sections[0];
    let mut rules: Vec<(u64, u64)> = vec![];

    for rule in raw_rules.iter() {
        let parts = rule.split("|").collect::<Vec<&str>>();
        rules.push((
            parts[0].parse::<u64>().unwrap(),
            parts[1].parse::<u64>().unwrap(),
        ));
    }

    let raw_updates = &sections[1];
    let mut updates: Vec<Vec<u64>> = vec![];

    for update in raw_updates.iter() {
        let parts = update.split(",").collect::<Vec<&str>>();
        let nums: Vec<u64> = parts
            .iter()
            .map(|val| val.parse::<u64>().unwrap())
            .collect::<Vec<u64>>();
        updates.push(nums);
    }

    println!(
        "Good Updates Values (Part 1): {}",
        handle_updates(&rules, &updates, false)
    );
    println!(
        "Bad Updates Values (Part 2): {}",
        handle_updates(&rules, &updates, true)
    );
}
