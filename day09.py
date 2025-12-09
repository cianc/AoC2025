import argparse
import copy
import itertools
import time

from typing import List, Tuple


def parse_input(filename: str) -> List[Tuple[int, int]]:
    tiles = []
    with open(filename, "r") as f:
        lines = [l.strip().split(',') for l in f.readlines()]
        for l in lines:
            tiles.append([int(l[0]), int(l[1])])

    return tiles

def square_contains_red_or_green_tile(corners: Tuple[Tuple[int, int], Tuple[int, int]], red_and_green_tiles: List[Tuple[int, int]]) -> bool:
    corner_1_x, corner_1_y = corners[0]
    corner_2_x, corner_2_y = corners[1]

    for tile_x, tile_y in red_and_green_tiles:
            if (corner_1_x < tile_x < corner_2_x) or (corner_2_x < tile_x < corner_1_x):
                if (corner_1_y < tile_y < corner_2_y) or (corner_2_y < tile_y < corner_1_y):
                    return True

    return False

def max_area(red_tiles: List[Tuple[int, int]]) -> int:
    max_area = 0
    for corners in itertools.combinations(red_tiles, 2):
        side1 = abs(corners[0][0] - corners[1][0]) + 1 
        side2 = abs(corners[0][1] - corners[1][1]) + 1
        area = side1 * side2
        if area > max_area:
            max_area = area

    return max_area

def red_and_green_tiles(red_tiles: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    red_and_green_tiles = copy.deepcopy(red_tiles)

    for tile in red_tiles:
        tile_x, tile_y = tile
        for other_tile in red_tiles:
            if tile == other_tile:
                continue
            other_tile_x, other_tile_y = other_tile
        
            if other_tile_y == tile_y:
                start_x, end_x = sorted([tile_x, other_tile_x])
                red_and_green_tiles.extend([offset, tile_y] for offset in range(start_x+1, end_x))


            if other_tile_x == tile_x:
                start_y, end_y = sorted([tile_y, other_tile_y])
                red_and_green_tiles.extend([tile_x, offset] for offset in range(start_y+1, end_y))

    return red_and_green_tiles


def max_area_only_green(red_tiles: List[Tuple[int, int]], red_and_green_tiles: List[Tuple[int, int]]) -> int:
    max_area = 0
    
    corners_to_check = len(list(itertools.combinations(red_tiles, 2)))
    for idx, corners in enumerate(itertools.combinations(red_tiles, 2)):
        if idx % 1000 == 0:
            print(f"{idx}/{corners_to_check}")
        if square_contains_red_or_green_tile(corners, red_and_green_tiles):
            continue
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

    red_tiles = parse_input(args.filename)

    part1_start_time = time.time()
    max_area = max_area(red_tiles)
    part1_end_time = time.time()

    print(f"part 1 answer: {max_area} - time: {part1_end_time - part1_start_time:e} seconds")
    
    ###################

    part2_start_time = time.time()
    red_and_green_tiles = red_and_green_tiles(red_tiles)    
    max_area = max_area_only_green(red_tiles, red_and_green_tiles)
    part2_end_time = time.time()

    print(f"part 2 answer: {max_area} - time: {part2_end_time - part2_start_time:e} seconds")


    
