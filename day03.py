import math
import re
import os
import sys
import time
import argparse

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

def _visualize_jolt_construction(battery_bank: list[int], n: int, window: list[tuple[int, int]], max_combination: list[int], chosen_digit: int):
    """Prints a single frame of the max jolt construction animation."""
    os.system('clear')
    
    bank_str = " ".join(map(str, battery_bank))
    
    window_vis = [' '] * (2 * len(battery_bank) - 1)
    if window:
        start_index = window[0][0]
        end_index = window[-1][0]
        for i in range(start_index, end_index + 1):
            window_vis[i*2] = '_'
            if i < end_index:
                window_vis[i*2 + 1] = '_'

    window_str = "".join(window_vis)

    print("--- Max Jolt Construction ---")
    print(f"Battery Bank:     {bank_str}")
    print(f"Search Window:    {window_str}")
    print(f"Digits to find:   {n - len(max_combination)}")
    print(f"Chosen digit:     {chosen_digit if chosen_digit is not None else '...'}")
    print(f"Max Combination:  {''.join(map(str, max_combination))}")
    print("-------------------------------")
    
    time.sleep(0.5)

def max_jolt_from_n_batteries(battery_bank: list[int], n: int, visualise: bool = False) -> int:
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

        if visualise:
            _visualize_jolt_construction(battery_bank, n, window, max_combination, max_battery)

        remaining_digits -= 1
        offset = max_position + 1

    max_jolt = 0
    for index, digit in enumerate(max_combination):
        max_jolt += 10**(n-index-1) * digit
    return max_jolt
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    parser.add_argument('--visualise', action='store_true', help="Enable visualisation for part 2.")
    args = parser.parse_args()

    batteries = parse_batteries(args.filename)

    start_part1_time = time.time()
    sorted_batteries = [sort_battery_bank(bank) for bank in batteries]
    total_jolt = 0
    for bank in sorted_batteries:
        max_jolt = max_jolt_from_2_batteries(bank)
        total_jolt += max_jolt
    end_part2_time = time.time()
    print(f"part 1 total jolt: {total_jolt} - time: {end_part2_time - start_part1_time:e} seconds")

    start_part2_time = time.time()
    total_jolt = 0
    for bank in batteries:
        total_jolt += max_jolt_from_n_batteries(bank, 12, visualise=args.visualise)
    end_part2_time = time.time()

    if args.visualise:
        # Print a final blank line to move past the animation
        print()

    print(f"part 2 total jolt: {total_jolt} - time: {end_part2_time - start_part2_time:e} seconds") 
