import argparse
import copy
import functools
import math
import time

from typing import List, Tuple

def create_jboxes_from_input(filename: str) -> dict:
    jboxes = {}
    with open(filename, 'r') as f:
        lines = [l.strip().split(',') for l in f.readlines()]
        for l in lines:
            jboxes[int(l[0]), int(l[1]), int(l[2])] = []
    return jboxes

def create_jbox_pairs_by_distance(jboxes: dict) -> List[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    pairs_to_distance = {}
    for jbox in jboxes.keys():
        for other_jbox in jboxes.keys():
            if jbox == other_jbox:
                continue
            if (other_jbox, jbox) in pairs_to_distance:
                continue
            pairs_to_distance[(jbox, other_jbox)] = math.dist(jbox, other_jbox)
            
    # Sort the pairs of elements by their distance in ascending order
    pairs_by_distance = [pair for pair, _ in sorted(pairs_to_distance.items(), key=lambda x: x[1])]
    return pairs_by_distance
    
def connect_nearest_n_jboxes(jboxes: dict, pairs_by_distance: List[Tuple[Tuple[int, ...], Tuple[int, ...]]], n: int) -> List[dict]:
    _jboxes = copy.deepcopy(jboxes)

    connections = 0
    while connections < n:
         for j1, j2 in pairs_by_distance:
             if j2 not in _jboxes[j1]:
                 _jboxes[j1].append(j2)
                 _jboxes[j2].append(j1)
                 connections += 1
                 break
    return _jboxes

def _recursive_count_circuit_size(jbox, jboxes, visited_jboxes):
    visited_jboxes.add(jbox)
    if not jboxes[jbox]:
        return 1, visited_jboxes
    
    count = 1
    for connected_jbox in jboxes[jbox]:
        if connected_jbox in visited_jboxes:
            continue
        visited_jboxes.add(connected_jbox)
        temp_count, visited_jboxes = _recursive_count_circuit_size(connected_jbox, jboxes, visited_jboxes)
        count += temp_count

    return count, visited_jboxes


def count_circuits(jboxes: dict) -> List[int]:
    circuit_sizes = []
    visited_jboxes = set()

    for jbox in jboxes.keys():
        if jbox in visited_jboxes:
            continue

        circuit_size, visited_jboxes = _recursive_count_circuit_size(jbox, jboxes, visited_jboxes)
        circuit_sizes.append(circuit_size)
           
    return circuit_sizes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    parser.add_argument('--connections', help="The number of junction box connections to make.", default=10, type=int)
    args = parser.parse_args()

    jboxes = create_jboxes_from_input(args.filename)

    part1_start_time = time.time()
    jbox_pairs_by_distance = create_jbox_pairs_by_distance(jboxes)
    connected_jboxes = connect_nearest_n_jboxes(jboxes, jbox_pairs_by_distance, args.connections)
    circuit_count = count_circuits(connected_jboxes)
    part1_end_time = time.time()

    print(f"part 1 answer: {functools.reduce(lambda x, y: x * y, sorted(circuit_count, reverse=True)[:3])} - time: {part1_end_time - part1_start_time:e} seconds")
