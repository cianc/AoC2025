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


def square_contains_red_or_green_tile_optimized(
    corners: Tuple[Tuple[int, int], Tuple[int, int]], 
    sorted_tiles: List[Tuple[int, int]], 
    sorted_tile_x_coords: List[int]
) -> bool:
    left_edge, right_edge = sorted([corners[0][0], corners[1][0]])
    bottom_edge, top_edge = sorted([corners[0][1], corners[1][1]])

    # Find the sub-list of tiles within the square's x-range using binary search
    start_index = bisect.bisect_right(sorted_tile_x_coords, left_edge)
    end_index = bisect.bisect_left(sorted_tile_x_coords, right_edge)

    # Now, only check the y-coordinates for this much smaller slice
    for i in range(start_index, end_index):
        _, tile_y = sorted_tiles[i]
        if bottom_edge < tile_y < top_edge:
            return True

    return False


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
    left_edge, right_edge = sorted([corners[0][0], corners[1][0]])
    bottom_edge, top_edge = sorted([corners[0][1], corners[1][1]])

    for tile_x, tile_y in red_and_green_tiles:
        if left_edge < tile_x < right_edge and bottom_edge < tile_y < top_edge:
            return True

    return False


@functools.cache
def _area(corners: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
    side1 = abs(corners[0][0] - corners[1][0]) + 1 
    side2 = abs(corners[0][1] - corners[1][1]) + 1
    return side1 * side2


def max_area_only_green(red_tiles: List[Tuple[int, int]], red_and_green_tiles: List[Tuple[int, int]]) -> int:
    max_area = 0

    sorted_red_and_green_tiles = sorted(red_and_green_tiles, key=lambda tile: tile[0])
    sorted_red_and_green_tiles_x_coords = [tile[0] for tile in sorted_red_and_green_tiles]
    
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
            #if square_contains_red_or_green_tile_optimized(corners, sorted_red_and_green_tiles, sorted_red_and_green_tiles_x_coords):
                continue
            else:
                max_area = area

    return max_area


def square_has_total_rg_overlap(corners: Tuple[Tuple[int, int], Tuple[int, int]], red_and_green_ranges: Dict[int, Tuple[int, int]]) -> bool:
    square_left_edge, square_right_edge = sorted([corners[0][0], corners[1][0]])
    square_top_edge, square_bottom_edge = sorted([corners[0][1], corners[1][1]])

    y_range = range(square_top_edge, square_bottom_edge + 1)

    # If the square has no height, it trivially satisfies the condition.
    if not y_range:
        return True

    try:
        # Instead of looping and checking each row, we can find the most restrictive
        # horizontal range across all rows the square occupies. This is done by finding
        # the maximum of all left boundaries and the minimum of all right boundaries.
        max_left_boundary = max(red_and_green_ranges[y][0] for y in y_range)
        min_right_boundary = min(red_and_green_ranges[y][1] for y in y_range)
    except KeyError:
        # If any y-coordinate of the square is not in the ranges dictionary,
        # it means there's no overlap, so we fail fast.
        return False

    # The entire square must fit within this single, most restrictive horizontal range.
    return square_left_edge >= max_left_boundary and square_right_edge <= min_right_boundary


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
    # Currently the fastest method.
    # Other methods implemented that are slower:
    #   max_area_only_green2(red_tiles, red_and_green_ranges): operates on ranges on their overlaps
    #   square_contains_red_or_green_tile_optimized() called from 
    #   that attempts to prune the range of tiles to check against.
    max_area = max_area_only_green(red_tiles, red_and_all_green_tiles)
    #red_and_green_ranges = red_and_green_full_ranges(red_and_all_green_tiles)
    #max_area = max_area_only_green(red_tiles, red_and_all_green_tiles)
    part2_end_time = time.time()

    print(f"part 2 answer: {max_area} - time: {part2_end_time - part2_start_time:e} seconds")

    
