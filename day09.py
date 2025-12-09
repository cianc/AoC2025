import argparse
import itertools
import time

from typing import List, Tuple


def parse_input(filename: str) -> List[Tuple[int, int]]:
    tiles = []
    with open(filename, "r") as f:
        lines = [l.strip().split(',') for l in f.readlines()]
        for l in lines:
            tiles.append((int(l[0]), int(l[1])))

    return tiles


def max_area(tiles: List[Tuple[int, int]]) -> int:
    max_area = 0
    for corners in itertools.combinations(tiles, 2):
        side1 = abs(corners[0][0] - corners[1][0]) + 1 
        side2 = abs(corners[0][1] - corners[1][1]) + 1
        area = side1 * side2
        if area > max_area:
            max_area = area

    return max_area



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The input file with battery banks.")
    parser.add_argument(
        "--visualise", action="store_true", help="Show visualisation for part 2."
    )
    args = parser.parse_args()

    tiles = parse_input(args.filename)

    part1_start_time = time.time()
    max_area = max_area(tiles)
    part1_end_time = time.time()

    print(f"part 1 answer: {max_area} - time: {part1_end_time - part1_start_time:e} seconds")
    




