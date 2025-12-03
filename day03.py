import math
import re
import sys
import time

def parse_batteries(file: str) -> list[list[int]]:
    batteries = []
    with open(file, 'r') as f:
        for line in f:
            battery_bank = [int(b) for b in line.strip()]
            batteries.append(battery_bank)

    return batteries

def sort_battery_bank(battery_bank: list[int]) -> list[(int, int)]:
    sorted_battery_bank = []
    for index, value in enumerate(battery_bank):
        sorted_battery_bank.append((value, index))

    sorted_battery_bank.sort(key=lambda x: x[0], reverse=True)
    return sorted_battery_bank

def max_jolt_from_2_batteries(sorted_battery_bank: list[(int, int)]) -> int:
    bank_length = len(sorted_battery_bank)
    max_battery, max_battery_position = sorted_battery_bank[0]

    # If max_battery is at the end of the bank, then it must be
    # the second jolt digit and the first is the next largest
    # battery.
    if max_battery_position == bank_length - 1: 
        jolt_second_digit = max_battery
        jolt_first_digit = sorted_battery_bank[1][0]
    # Otherwise, max_battery is the first jolt digit and the
    # second digit is the largest battery to its right.
    else:
        jolt_first_digit = max_battery
        batteries_to_right = [battery for battery in sorted_battery_bank if battery[1] > max_battery_position]
        jolt_second_digit = max(batteries_to_right, key=lambda x: x[0])[0]
        
    return int(str(jolt_first_digit) + str(jolt_second_digit))

def max_jolt_from_n_batteries(battery_bank: list[(int, int)], n: int) -> int:
    indexed_battery_bank = list(enumerate(battery_bank))

    max_combination = []
    window_size = len(battery_bank) - n + 1
    offset = 0
    remaining_digits = n
    while len(max_combination) < n:
        window_size = len(battery_bank) - offset - remaining_digits + 1
        window = indexed_battery_bank[offset:offset+window_size]
        # This sorts from biggest to smallest battery value, and earliest to latest
        # position within identical values. This lets us pick the highest earliest value.
        sorted_window = sorted(window, key=lambda x: (-x[1], x[0]))
        max_position, max_battery = sorted_window[0]
        max_combination.append(max_battery)
        remaining_digits -= 1
        offset = max_position + 1

    max_jolt = 0
    for index, digit in enumerate(max_combination):
        max_jolt += 10**(n-index-1) * digit
    return max_jolt


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        raise ValueError('Missing filename argument.')

    batteries = parse_batteries(filename)

    start_part1_time = time.time()
    sorted_batteries = [sort_battery_bank(bank) for bank in batteries]
    total_jolt = 0
    for battery_bank in sorted_batteries:
        max_jolt = max_jolt_from_2_batteries(battery_bank)
        total_jolt += max_jolt
    end_part2_time = time.time()

    print(f"part 1 total jolt: {total_jolt} - time: {end_part2_time - start_part1_time:e} seconds")

    start_part2_time = time.time()
    total_jolt = 0
    for bank in batteries:
        total_jolt += max_jolt_from_n_batteries(bank, 12)
    end_part2_time = time.time()

    print(f"part 2 total jolt: {total_jolt} - time: {end_part2_time - start_part2_time:e} seconds") 
