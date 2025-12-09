import argparse
import bisect
import copy
import functools
import itertools
import math
import time

from typing import List, Tuple, Dict, Set


def parse_input(filename: str) -> List[Tuple[int, int]]:
    tiles = []
    with open(filename, "r") as f:
        lines = [l.strip().split(',') for l in f.readlines()]
        for l in lines:
            tiles.append((int(l[0]), int(l[1])))

    return tiles

def max_area(red_tiles: List[Tuple[int, int]]) -> int:
    max_area = 0
    for corners in itertools.combinations(red_tiles, 2):
        side1 = abs(corners[0][0] - corners[1][0]) + 1 
        side2 = abs(corners[0][1] - corners[1][1]) + 1
        area = side1 * side2
        if area > max_area:
            max_area = area

    return max_area
    
def red_and_green_edge_tiles(red_tiles: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    red_and_green_tiles = copy.deepcopy(red_tiles)

    for tile in red_tiles:
        tile_x, tile_y = tile
        for other_tile in red_tiles:
            if tile == other_tile:
                continue
            other_tile_x, other_tile_y = other_tile
        
            if other_tile_y == tile_y:
                start_x, end_x = sorted([tile_x, other_tile_x])
                red_and_green_tiles.extend((offset, tile_y) for offset in range(start_x+1, end_x))


            if other_tile_x == tile_x:
                start_y, end_y = sorted([tile_y, other_tile_y])
                red_and_green_tiles.extend((tile_x, offset) for offset in range(start_y+1, end_y))

    return red_and_green_tiles


def red_and_green_full_ranges(red_and_green_edge_tiles: List[Tuple[int, int]]) -> Dict[int, Tuple[int, int]]:
    red_and_green_full_ranges = {}
    for edge_tile in red_and_green_edge_tiles:
        tile_x, tile_y = edge_tile
        if tile_y not in red_and_green_full_ranges:
            red_and_green_full_ranges[tile_y] = set([tile_x])
        else:
            red_and_green_full_ranges[tile_y].add(tile_x)
    
    for row in red_and_green_full_ranges:
        start, end = min(red_and_green_full_ranges[row]), max(red_and_green_full_ranges[row])
        red_and_green_full_ranges[row] = (start, end)

    return red_and_green_full_ranges



def square_contains_red_or_green_tile(corners: Tuple[Tuple[int, int], Tuple[int, int]], red_and_green_tiles: List[Tuple[int, int]]) -> bool:
    corner_1_x, corner_1_y = corners[0]
    corner_2_x, corner_2_y = corners[1]

    for tile_x, tile_y in red_and_green_tiles:
            if (corner_1_x < tile_x < corner_2_x) or (corner_2_x < tile_x < corner_1_x):
                if (corner_1_y < tile_y < corner_2_y) or (corner_2_y < tile_y < corner_1_y):
                    return True

    return False


@functools.cache
def _area(corners: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
    side1 = abs(corners[0][0] - corners[1][0]) + 1 
    side2 = abs(corners[0][1] - corners[1][1]) + 1
    return side1 * side2


def max_area_only_green(red_tiles: List[Tuple[int, int]], red_and_green_tiles: List[Tuple[int, int]]) -> int:
    max_area = 0
    
    # Sort descending by distance between points since these are more likely to
    # cover larger squars and so create a new max.
    corners_to_check = list(itertools.combinations(red_tiles, 2))
    corners_to_check = sorted(corners_to_check, key=lambda corners: math.dist(corners[0], corners[1]), reverse=True)
    for idx, corners in enumerate(corners_to_check):
        if idx % 1000 == 0:
            print(f"{idx}/{len(corners_to_check)}")

        area = _area(corners)
        if area > max_area:            
            if square_contains_red_or_green_tile(corners, red_and_green_tiles):
                continue
            else:
                max_area = area

    return max_area


def square_has_total_rg_overlap(corners: Tuple[Tuple[int, int], Tuple[int, int]], red_and_green_ranges: Dict[int, Tuple[int, int]]) -> bool:
    square_left_edge, square_right_edge = sorted([corners[0][0], corners[1][0]])
    square_top_edge, square_bottom_edge = sorted([corners[0][1], corners[1][1]])

    for y in range(square_top_edge, square_bottom_edge+1):
        if not red_and_green_ranges[y][0] <= square_left_edge <= red_and_green_ranges[y][1]:
            return False
        if not red_and_green_ranges[y][0] <= square_right_edge <= red_and_green_ranges[y][1]:
            return False

    return True


def max_area_only_green2(red_tiles: List[Tuple[int, int]], red_and_green_ranges: Dict[int, Tuple[int, int]]) -> int:
    max_area = 0
    
    # Sort descending by distance between points since these are more likely to
    # cover larger squars and so create a new max.
    corners_to_check = list(itertools.combinations(red_tiles, 2))
    corners_to_check = sorted(corners_to_check, key=lambda corners: math.dist(corners[0], corners[1]), reverse=True)
    for idx, corners in enumerate(corners_to_check):
        if idx % 1000 == 0:
            print(f"{idx}/{len(corners_to_check)}")

        area = _area(corners)
        if area > max_area:            
            if square_has_total_rg_overlap(corners, red_and_green_ranges):
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
    red_and_all_green_tiles = red_and_green_edge_tiles(red_tiles)
    red_and_green_ranges = red_and_green_full_ranges(red_and_all_green_tiles)
    max_area = max_area_only_green2(red_tiles, red_and_green_ranges)
    part2_end_time = time.time()

    print(f"part 2 answer: {max_area} - time: {part2_end_time - part2_start_time:e} seconds")

    
