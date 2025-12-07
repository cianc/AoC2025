import argparse
import copy
import time

from typing import List, Tuple


def parse_manifold(filename: str) -> List[str]:
    manifold = []
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        for line in lines:
            manifold.append([c for c in line])

    return manifold


def plot_classical_beam(manifold: List[str]) -> Tuple[List[str], int]:
    plot = copy.deepcopy(manifold)
    plot_width = len(plot[0])
    plot_depth = len(plot)
    split_count = 0 

    for r_idx, row in enumerate(plot):
        for c_idx, c in enumerate(row):
            if c in ('|', 'S'):
                if r_idx + 1 < plot_depth:
                    if plot[r_idx+1][c_idx] == '^':
                        split_count += 1
                        if c_idx - 1 >= 0:
                            plot[r_idx+1][c_idx - 1] = '|' 
                        if c_idx + 1 < plot_width:
                            plot[r_idx+1][c_idx + 1] = '|'
                    else:
                        plot[r_idx+1][c_idx] = '|'
                

    return plot, split_count


def plot_quantum_beam(manifold: List[str]) -> int:
    manifold_width = len(manifold[0])
    manifold_depth = len(manifold)
    #print(f"manifold_depth: {manifold_depth}")
    #for row in manifold:
    #    print(''.join(row))
    #print('=================')


    if manifold_depth == 1:
     #   time.sleep(0.5)
        return 1

    timeline_count = 0

    for c_idx, c in enumerate(manifold[0]):
        #print(f"c_idx: {c_idx}, c: {c}")
        if c in ('|', 'S'):
            if manifold[1][c_idx] == '^':
                if c_idx - 1 >= 0:
                    manifold[1][c_idx - 1] = '|' 
                    timeline_count += plot_quantum_beam(manifold[1:])
                    manifold[1][c_idx - 1] = '.'
                    #print(f"manifold_depth2: {manifold_depth} - timeline_count: {timeline_count}")
                if c_idx + 1 < manifold_width:
                    manifold[1][c_idx + 1] = '|'
                    timeline_count += plot_quantum_beam(manifold[1:])
                    manifold[1][c_idx + 1] = '.'
                    #print(f"manifold_depth3: {manifold_depth} - timeline_count: {timeline_count}")
                
            else:
                manifold[1][c_idx] = '|'
                timeline_count += plot_quantum_beam(manifold[1:])
                manifold[1][c_idx] = '.'
                #print(f"manifold_depth4: {manifold_depth} - timeline_count: {timeline_count}")
    #print(f"Finished manifold_depth: {manifold_depth} - timeline_count: {timeline_count}")


    #time.sleep(0.5)
    return timeline_count






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The input file with battery banks.")
    parser.add_argument(
        "--visualise", action="store_true", help="Show visualisation for part 2."
    )
    args = parser.parse_args()

    part1_start = time.time()
    manifold = parse_manifold(args.filename)
    beam_plot, split_count = plot_classical_beam(manifold)
    part1_end = time.time()

    print(f"part1 answer: {split_count} - time: {part1_end - part1_start:e}")

    #################

    part2_start = time.time()
    timeline_count = plot_quantum_beam(manifold)
    part2_end = time.time()

    print(f"part2 answer: {timeline_count} - time: {part2_end - part2_start:e}")