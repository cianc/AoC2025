import argparse
import itertools
import time

from typing import List, Tuple


DELTAS = list(itertools.product((-1, 0, 1), repeat=2))
DELTAS.remove((0, 0))


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
    args = parser.parse_args()

    warehouse, rolls = parse_input(args.filename)

    part1_start_time = time.time()
    accessible_roll_count, _, _ = count_and_remove_accessible_rolls(warehouse, rolls)
    part1_end_time = time.time()

    print(f"part 1 accessible rolls: {accessible_roll_count} - time taken: {part1_end_time - part1_start_time:e}")

    ###################

    warehouse, rolls = parse_input(args.filename)
    original_roll_count = len(rolls)

    part2_start_time = time.time()
    previous_roll_count = original_roll_count
    while True:
        accessible_roll_count, warehouse, rolls = count_and_remove_accessible_rolls(warehouse, rolls)
        # for row in warehouse:
        #     print(''.join(row))
        # print(f"removed rolls: {previous_roll_count - len(rolls)}")
        # print('#' * 80)
        if len(rolls) == previous_roll_count:
            break
        previous_roll_count = len(rolls)
    part2_end_time = time.time()
    
    print(f"part 2 - removed rolls: {original_roll_count - len(rolls)} - time taken: {part2_end_time - part2_start_time:e}")