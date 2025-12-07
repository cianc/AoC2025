import argparse
import copy
import time

from typing import List, Tuple, Union


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

def visualize_timeline_evolution(beam_plot: List[str], history: List[List[int]], timeline_count: int):
    """
    Prints the step-by-step evolution of quantum timelines.
    """
    print("\nVisualizing quantum timeline evolution...")

    print("\nBeam Plot for context:")
    for row in beam_plot:
        print("".join(row))

    print("\nTimeline distribution at each split:")
    for i, distrib in enumerate(history):
        line = f"Step {i:02d}: "
        for val in distrib:
            if val == 0:
                line += "     . "
            else:
                line += f"{val: >6d} "
        print(line)

    print(f"\nFinal timeline count from visualization: {timeline_count}")


def count_quantum_timelines(beam_plot: List[str], get_history: bool = False) -> Union[int, Tuple[int, List[List[int]]]]:
    '''
    At first I tried to solve this with a regular DFS to walk all possible
    paths and count them. It was very slow, probably caching would have
    helped.
    This approach is much more straight forward. Start at the top of the
    grid, go down row by row, keeping track of all splits and adjusting
    possible path counts as we go. Paths (plural, because we can and do have
    multiple overlapping paths) hitting a splitter create paths on each
    side (assuming we're not at an edge).
    '''
    timelines = [int(c == 'S') for c in beam_plot[0]]
    history = [list(timelines)] if get_history else None

    for row_idx, row in enumerate(beam_plot):
        for c_idx, c in enumerate(row):
             if c in ('|', 'S'):
                 if row_idx + 1 < len(beam_plot):
                     if beam_plot[row_idx+1][c_idx] == '^':
                        if timelines[c_idx] > 0:
                            if c_idx - 1 >= 0:
                                timelines[c_idx - 1] += timelines[c_idx]
                            if c_idx + 1 < len(row):
                                timelines[c_idx + 1] += timelines[c_idx]
                            timelines[c_idx] = 0
                            if get_history:
                                history.append(list(timelines))

    total_timelines = sum(timelines)
    if get_history:
        return total_timelines, history
    return total_timelines
                 

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
    if args.visualise:
        timeline_count, history = count_quantum_timelines(beam_plot, get_history=True)
        visualize_timeline_evolution(beam_plot, history, timeline_count)
    else:
        timeline_count = count_quantum_timelines(beam_plot)
    part2_end = time.time()

    print(f"part2 answer: {timeline_count} - time: {part2_end - part2_start:e}")