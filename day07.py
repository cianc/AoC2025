import argparse
import copy

from typing import List, Tuple


def parse_manifold(filename: str) -> List[str]:
    manifold = []
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        for line in lines:
            manifold.append([c for c in line])

    return manifold


def plot_beam(manifold: List[str]) -> Tuple[List[str], int]:
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The input file with battery banks.")
    parser.add_argument(
        "--visualise", action="store_true", help="Show visualisation for part 2."
    )
    args = parser.parse_args()

    manifold = parse_manifold(args.filename)
    beam_plot, split_count = plot_beam(manifold)

    print(f"answer: {split_count}")