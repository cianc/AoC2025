import argparse
import copy
import itertools
import re
import time

TREE_RE = r'\d+x\d+\:((\ \d+)+)'

from typing import List, Tuple, Dict



def parse_input(filename: str) -> Tuple[List[List[str]], List[Tuple[List[int], List[int]]]]:
    shapes = []
    trees = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break

            if re.match(r'^\d\:', line):
                shapes.append([])
                while True:
                    shape_line = f.readline()
                    if shape_line == '\n':
                        break
                    shapes[-1].append([c for c in shape_line.strip()])
                continue

            m = re.match(TREE_RE, line)
            if m:
                dims, presents = line.split(':')
                dims = [int(dim) for dim in dims.strip().split('x')]
                presents = [int(present) for present in presents.strip().split(' ')]
                trees.append((dims, presents))

    return shapes, trees


def _horizontal_flip(shape: List[List[str]]) -> List[List[str]]:
    return [row[::-1] for row in shape]


# A 90 degree rotation is equal to a transpose and a vertical flip
def _90_degree_rotation(shape: List[List[str]]) -> List[List[str]]:
    transposed = list(map(list, zip(*shape)))
    return transposed[::-1]


def all_translated_shapes(shapes: List[List[str]]) -> Dict[int, List[List[str]]]:
    all_translated_shapes = {}
    for idx, shape in enumerate(shapes):
        translated_shapes = []
        for _ in range(4):
            translated_shapes.append(shape)
            translated_shapes.append(_horizontal_flip(shape))
            shape = _90_degree_rotation(shape)

        all_translated_shapes[idx] = translated_shapes
        
    return all_translated_shapes
    

def shape_fits_at_square(shape: List[List[str]], grid: List[List[str]], start_row_idx: int, start_col_idx: int, present_id: int) -> Tuple[bool, List[List[str]]]:
    for row_idx, row in enumerate(shape):
        shape_cols = [col_idx for col_idx, s in enumerate(row) if s == '#']
        if shape_cols:
            bottom_left_offset = (row_idx, min(shape_cols))
            break

    grid_copy = copy.deepcopy(grid)
    for row_idx, row in enumerate(shape):
        for c_idx, c in enumerate(row):
            if c == '#':
                if start_row_idx + row_idx - bottom_left_offset[0] >= len(grid):
                    return False, grid
                if start_col_idx + c_idx - bottom_left_offset[1] >= len(grid[0]):
                    return False, grid
                if grid[start_row_idx + row_idx - bottom_left_offset[0]][start_col_idx + c_idx - bottom_left_offset[1]] != '.':
                    return False, grid
                else:
                    grid_copy[start_row_idx + row_idx - bottom_left_offset[0]][start_col_idx + c_idx - bottom_left_offset[1]] = str(present_id)


    return True, grid_copy



def part1(all_translated_shapes: Dict[List[List[str]]], trees: List[Tuple[List[int], List[int]]]) -> int:
    '''
    Does not work on test input
    '''
    success_counter = 0
    for tree_idx, tree in enumerate(trees):
        print(f"tree {tree_idx}/{len(trees)}")
        
        width, depth = tree[0]
        grid = [['.' for _ in range(width)] for _ in range(depth)]
        presents = tree[1]
        presents_counter = dict(enumerate(presents))
    
        while True:

            success = False
            for row_idx, row in enumerate(grid):
                for c_idx, square in enumerate(row):
                    if square == '.':
                        for present_id in [p for p, c in presents_counter.items() if c > 0]:
                            for shape in all_translated_shapes[present_id]:
                                fits, grid = shape_fits_at_square(shape, grid, row_idx, c_idx, present_id)
                                if fits:
                                    presents_counter[present_id] -= 1
                                    success = True
                                    break
                            else:
                                continue
                            break
                        else:
                            continue
                        break
                else:
                    continue
                break


            if success == False:
                break
            
            if all(v == 0 for v in presents_counter.values()):
                success_counter += 1
                break

    return success_counter
    

def part1_trivial(shapes, trees):
    '''
    I can't believe this worked on the real puzzle input (but fails on the test input)
    '''
    succeess_counter = 0
    for tree in trees:
        area_available = tree[0][0] * tree[0][1]
        presents = tree[1]
        area_needed = sum(presents) * 9
        print(f"area_available: {area_available}, area_needed: {area_needed}")
        if area_needed <= area_available:
            succeess_counter += 1

    return succeess_counter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    parser.add_argument('--visualise', action='store_true', help="Show visualisation for part 2.")
    args = parser.parse_args()

    shapes, trees = parse_input(args.filename)
    all_translated_shapes = all_translated_shapes(shapes)

    part1_start_time = time.time()
    answer = part1(all_translated_shapes, trees)
    part1_end_time = time.time()
    print(f"part 1 answer: {answer} - time: {part1_end_time - part1_start_time:e} seconds")