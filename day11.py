import argparse
import functools
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


def part1(nodes: Dict[str, List[str]]) -> int:
    @functools.cache
    def _recurse(node: str, target: str) -> int:
        if node == target:
            return 1
        
        path_count = 0
        for child in nodes[node]:
            path_count += _recurse(child, target)
        return path_count

    return _recurse('you', 'out')


def part2(nodes: Dict[str, List[str]]) -> int:
    @functools.cache
    def _recurse(node: str, target: str, avoid: Tuple[str]) -> int:
        if node == target:
            return 1
        if node in avoid:
            return 0
        
        path_count = 0
        for child in nodes[node]:
            path_count += _recurse(child, target, avoid)
        return path_count
    
    svr_to_fft_count = _recurse('svr', 'fft', ('out', 'dac'))
    print(f"svr_to_fft_count: {svr_to_fft_count}")
    fft_to_dac_count = _recurse('fft', 'dac', ('out', 'svr'))
    print(f"fft_to_dac_count: {fft_to_dac_count}")
    dac_to_out_count = _recurse('dac', 'out', ('fft', 'svr'))
    print(f"dac_to_out_count: {dac_to_out_count}")

    return svr_to_fft_count * fft_to_dac_count * dac_to_out_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    parser.add_argument('--part', help="Which part to run, default to both.", default=0, type=int)
    parser.add_argument('--visualise', action='store_true', help="Show visualisation for part 2.")
    args = parser.parse_args()

    nodes = parse_input(args.filename)
    for node in nodes.items():
        print(node)

    if args.part in (0, 1):
        part1_start_time = time.time()
        answer = part1(nodes)
        part1_end_time = time.time()

        print(f"part 1 answer: {answer} - time: {part1_end_time - part1_start_time:e} seconds")

    #######################

    if args.part in (0, 2):
        part2_start_time = time.time()
        answer = part2(nodes)
        part2_end_time = time.time()

        print(f"part 2 answer: {answer} - time: {part2_end_time - part2_start_time:e} seconds")