import argparse
import time

from typing import List, Tuple, Dict

def parse_input(filename: str) -> Dict[str, List[str]]:
    nodes = {}
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        for line in lines:
            src, dsts = line.split(':')
            dsts = dsts.split()

            nodes[src] = dsts

    return nodes

def _recurse_part1(node: str, nodes: Dict[str, List[str]]) -> int:
    if node == 'out':
        return 1
    
    path_count = 0
    for child in nodes[node]:
        path_count  += _recurse_part1(child, nodes)

    return path_count


def part1(nodes: Dict[str, List[str]]) -> int:
    path_count = _recurse_part1('you', nodes)
    return path_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    parser.add_argument('--visualise', action='store_true', help="Show visualisation for part 2.")
    args = parser.parse_args()

    nodes = parse_input(args.filename)
    for node in nodes.items():
        print(node)

    part1_start_time = time.time()
    answer = part1(nodes)
    part1_end_time = time.time()

    print(f"part 1 answer: {answer} - time: {part1_end_time - part1_start_time:e} seconds")