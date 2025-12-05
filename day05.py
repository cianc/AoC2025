import argparse
import os
import sys
import time

from typing import List, Tuple

def parse_inventory(filename: str) -> Tuple[List[List[int]], List[int]]:
    fresh_ranges = []
    ingredients = []
    with open(filename, 'r') as f:
        in_ranges = True
        for line in f.readlines():
            line = line.strip()
            if not line:
                in_ranges = False
                continue
            if in_ranges:  
                start, stop = line.split('-')
                fresh_ranges.append([int(start), int(stop)])
            else:
                ingredients.append(int(line.strip()))

    return fresh_ranges, ingredients

def merge_ranges(ranges: List[List[int]]) -> List[List[int]]:
    ranges.sort(key=lambda x: x[0])
    merged_ranges = [ranges[0]]
    for start, stop in ranges[1:]:
        last_start, last_stop = merged_ranges[-1]
        if start <= last_stop:
            merged_ranges[-1] = [last_start, max(last_stop, stop)]
        else:
            merged_ranges.append([start, stop])

    return merged_ranges


def fresh_or_spoiled(fresh_ranges: List[List[int]], ingredients: List[int]) -> Tuple[List[int], List[int]]:
    fresh = []
    spoiled = []
    for ingredient in ingredients:
        for start, stop in fresh_ranges:
            if start <= ingredient <= stop:
                fresh.append(ingredient)
                break
        else:
            spoiled.append(ingredient)

    return fresh, spoiled

def count_all_possible_fresh_ingredients(fresh_ranges: List[List[int]]) -> int:
    count = 0 
    for start, stop in fresh_ranges:
        count += stop - start + 1
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    parser.add_argument('--visualise', action='store_true', help="Show visualisation for part 2.")
    args = parser.parse_args()

    fresh_ranges, ingredients = parse_inventory(args.filename)
    
    part1_start_time = time.time()
    merged_fresh_ranges = merge_ranges(fresh_ranges)
    fresh, spoiled = fresh_or_spoiled(merged_fresh_ranges, ingredients)
    part1_end_time = time.time()

    print(f"count of fresh ingredients: {len(fresh)} - time: {part1_end_time - part1_start_time:e}")

    ###################

    part2_start_time = time.time()
    total_possible_fresh_count = count_all_possible_fresh_ingredients(merged_fresh_ranges)
    part2_end_time = time.time()

    print(f"total possible fresh ingredients: {total_possible_fresh_count} - time: {part2_end_time - part2_start_time:e}")