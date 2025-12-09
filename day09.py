import argparse
import bisect
import copy
import functools
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
                red_and_green_tiles.extend((offset, tile_y) for offset in range(start_x+1, end_x))


            if other_tile_x == tile_x:
                start_y, end_y = sorted([tile_y, other_tile_y])
                red_and_green_tiles.extend((tile_x, offset) for offset in range(start_y+1, end_y))

    return red_and_green_tiles

@functools.cache
def _area(corners: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
    side1 = abs(corners[0][0] - corners[1][0]) + 1 
    side2 = abs(corners[0][1] - corners[1][1]) + 1
    return side1 * side2

def max_area_only_green(red_tiles: List[Tuple[int, int]], red_and_green_tiles: List[Tuple[int, int]]) -> int:
    max_area = 0
    
    corners_to_check = len(list(itertools.combinations(red_tiles, 2)))
    for idx, corners in enumerate(itertools.combinations(red_tiles, 2)):
        if idx % 1000 == 0:
            print(f"{idx}/{corners_to_check}")
        if corners[0][0] == corners[1][0] or corners[0][1] == corners[1][1]:
            continue

        area = _area(corners)
        if area > max_area:            
            if square_contains_red_or_green_tile(corners, red_and_green_tiles):
                continue
            else:
                max_area = area

    return max_area

def _red_and_green_tiles_of_interest(corners: Tuple[Tuple[int, int], Tuple[int, int]], red_and_green_tiles: List[Tuple[int, int]]):
    leftmost_corner, rightmost_corner = sorted(corners, key=lambda t: t[0])
    top_corner, bottom_corner = sorted(corners, key=lambda t: t[1])


    tiles_of_interest = [tile for tile in red_and_green_tiles if (leftmost_corner[0] < tile[0] < rightmost_corner[0]) and (top_corner[1] < tile[1] < bottom_corner[1])]
    return tiles_of_interest
   
   
    #idx = bisect.bisect_right(red_and_green_tiles_sorted_by_x, ingredient)


def max_area_only_green2(red_tiles: List[Tuple[int, int]], red_and_green_tiles: List[Tuple[int, int]]) -> int:
    max_area = 0

    red_and_green_tiles_sorted_by_x = sorted(red_and_green_tiles, key=lambda t: t[0])
    red_and_green_tiles_sorted_by_y = sorted(red_and_green_tiles, key=lambda t: t[1])

    corners_to_check = list(itertools.combinations(red_tiles, 2))
    for idx, corners in enumerate(corners_to_check):
        if idx % 1000 == 0:
            print(f"{idx}/{len(corners_to_check)}")
        if corners[0][0] == corners[1][0] or corners[0][1] == corners[1][1]:
            continue

        area = _area(corners)
        if area > max_area:            
            
            leftmost_corner, rightmost_corner = sorted(corners, key=lambda t: t[0])
            top_corner, bottom_corner = sorted(corners, key=lambda t: t[1])

            leftmost_idx = bisect.bisect_right(red_and_green_tiles_sorted_by_x, leftmost_corner[0], key=lambda t: t[0])
            #leftmost_idx = red_and_green_tiles_sorted_by_x.index(leftmost_corner)+1
            rightmost_idx = bisect.bisect_left(red_and_green_tiles_sorted_by_x, rightmost_corner[0], key=lambda t: t[0])
            #rightmost_idx = red_and_green_tiles_sorted_by_x.index(rightmost_corner)
            topmost_idx = bisect.bisect_right(red_and_green_tiles_sorted_by_y, top_corner[1], key=lambda t: t[1])
            #topmost_idx = red_and_green_tiles_sorted_by_y.index(top_corner)+1
            bottommost_idx = bisect.bisect_left(red_and_green_tiles_sorted_by_y, bottom_corner[1], key=lambda t: t[1])
            #bottommost_idx = red_and_green_tiles_sorted_by_y.index(bottom_corner)
            
            tiles_of_interest = set(red_and_green_tiles_sorted_by_x[leftmost_idx:rightmost_idx])
            tiles_of_interest = tiles_of_interest.intersection(
                set(red_and_green_tiles_sorted_by_y[topmost_idx:bottommost_idx]))
            tiles_of_interest = list(tiles_of_interest)

            if tiles_of_interest:
                continue
            else:
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


    
