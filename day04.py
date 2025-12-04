import argparse
import itertools
import os
import time

from typing import List, Tuple


DELTAS = list(itertools.product((-1, 0, 1), repeat=2))
DELTAS.remove((0, 0))


def print_warehouse(warehouse: List[List[str]], removed_roll_count: int):
    os.system('clear')
    for row in warehouse:
        print("".join(row))
    if warehouse and warehouse[0]:
        print("-" * len(warehouse[0]))
    print(f"\nRemoved {removed_roll_count} rolls")
    time.sleep(0.5)


def parse_input(filename: str) -> Tuple[List[List[str]], List[Tuple[int, int]]]:
    warehouse = []
    rolls = []
    with open(filename, 'r') as f:
        for row_index, line in enumerate(f.readlines()):
            row_data = list(line.strip())
            warehouse.append(row_data)
            for char_index, char in enumerate(row_data):
                if char == '@':
                    rolls.append((row_index, char_index))
            
    return warehouse, rolls

def count_and_remove_accessible_rolls(warehouse: List[List[str]], rolls: List[Tuple[int, int]]) -> Tuple[int, List[List[str]], List[Tuple[int, int]]]:
    rolls_to_remove = []
    max_row_index = len(warehouse) - 1
    num_col_index = len(warehouse[0]) - 1

    for roll in rolls:
        row_index, col_index = roll

        other_rolls_count = 0
        for row_delta, col_delta in DELTAS:
            new_row_index = row_index + row_delta
            new_col_index = col_index + col_delta

            if not (0 <= new_row_index <= max_row_index and 0 <= new_col_index <= num_col_index):
                continue
            if warehouse[new_row_index][new_col_index] == '@':
                other_rolls_count += 1
                if other_rolls_count >= 4:
                    break
        
        if other_rolls_count < 4:
            rolls_to_remove.append(roll)
    
    if not rolls_to_remove:
        return 0, warehouse, rolls

    for row_index, col_index in rolls_to_remove:
        warehouse[row_index][col_index] = '.'

    rolls_to_remove_set = set(rolls_to_remove)
    new_rolls = [roll for roll in rolls if roll not in rolls_to_remove_set]
    
    return len(rolls_to_remove), warehouse, new_rolls


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    parser.add_argument('--visualise', action='store_true', help="Show visualisation for part 2.")
    args = parser.parse_args()

    warehouse, rolls = parse_input(args.filename)

    part1_start_time = time.time()
    # Run part 1 on a copy of the warehouse to show visualization without affecting the original variable before re-parsing
    p1_warehouse = [row[:] for row in warehouse]
    accessible_roll_count, p1_warehouse, _ = count_and_remove_accessible_rolls(p1_warehouse, rolls)
    part1_end_time = time.time()

    print(f"part 1 accessible rolls: {accessible_roll_count} - time taken: {part1_end_time - part1_start_time:e}")

    ###################

    warehouse, rolls = parse_input(args.filename)
    original_roll_count = len(rolls)
    if args.visualise:
        print("\nStarting Part 2. Initial state:")
        print_warehouse(warehouse, 0)

    part2_start_time = time.time()
    previous_roll_count = original_roll_count
    step = 0
    while True:
        step += 1
        removed_roll_count, warehouse, rolls = count_and_remove_accessible_rolls(warehouse, rolls)
        
        if len(rolls) == previous_roll_count:
            break
        
        if args.visualise:
            print_warehouse(warehouse, removed_roll_count)

        previous_roll_count = len(rolls)
    part2_end_time = time.time()
    
    print(f"part 2 - removed rolls: {original_roll_count - len(rolls)} - time taken: {part2_end_time - part2_start_time:e}")
