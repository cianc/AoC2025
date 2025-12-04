import argparse
import itertools
import time

from typing import List, Tuple


def parse_input(filename: str) -> Tuple[List[List[str]], List[Tuple[int, int]]]:
    warehouse = []
    rolls = []
    with open(filename, 'r') as f:
        for row_index, line in enumerate(f.readlines()):
            warehouse.append([])
            for char_index, char in enumerate(line.strip()):
                if char == '@':
                    rolls.append((row_index, char_index))
                if not warehouse[row_index]:
                    warehouse[row_index] = [char]
                else:
                    warehouse[row_index].append(char)
            
    return warehouse, rolls

def count_and_remove_accessible_rolls(warehouse: List[str], rolls: List[int]) -> Tuple[int, List[str], List[int]]:
    accessible_roll_count = 0
    rolls_to_remove = []

    for roll in rolls:
        row_index, col_index = roll
        max_row_index = len(warehouse) - 1
        num_col_index = len(warehouse[0]) - 1

        deltas = list(itertools.product((-1, 0, 1), repeat=2))
        deltas.remove((0, 0))
        other_rolls_count = 0
        for row_delta, col_delta in deltas:
            new_row_index = row_index + row_delta
            new_col_index = col_index + col_delta

            if new_row_index < 0 or new_row_index > max_row_index or new_col_index < 0 or new_col_index > num_col_index:
                continue
            if warehouse[new_row_index][new_col_index] == '@':
                other_rolls_count += 1
        
        if other_rolls_count < 4:
            accessible_roll_count += 1
            rolls_to_remove.append(roll)
    
    for roll in rolls_to_remove:
        rolls.remove(roll)
        warehouse[roll[0]][roll[1]] = '.'
    
    return accessible_roll_count, warehouse, rolls



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
