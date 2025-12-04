import argparse
import itertools
import time

def parse_input(filename: str) -> tuple[list[list[str]], list[tuple[int, int]]]:
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

def count_accessible_rolls(warehouse: list[str], rolls: list[int]) -> int:
    accessible_roll_count = 0

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
    
    return accessible_roll_count




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    args = parser.parse_args()

    warehouse, rolls = parse_input(args.filename)

    part1_start_time = time.time()
    accessible_roll_count = count_accessible_rolls(warehouse, rolls)
    part1_end_time = time.time()
    
    print(f"accessible rolls: {accessible_roll_count} - time taken: {part1_end_time - part1_start_time:e}")