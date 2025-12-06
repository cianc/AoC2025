import argparse
import functools
import time

from typing import List, Tuple


def part1(filename: str) -> List:
    '''
    We read the file in reverse to see the relevant operator for
    each column and then maintain a running total as we read backwards.
    As opposed to reading forwards, storging each number and only
    peforming the calculation at the end.
    In theory this reduces memory usage, but doesn't really because
    we're doing the lazy thing of reading all lines into memory to reverse
    their order. We could do a proper backwards scan if wanted to do
    it right.
    Another option would be to scan forwards and maintain two answers for
    each column, one for * and one for + and then pick the right one at
    the end.
    '''
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines.reverse()
        answers = [[op] for op in lines[0].strip().split()]
        for idx, number in enumerate(lines[1].strip().split()):
            answers[idx].append(int(number))

        for line in lines[2:]:
            for idx, number in enumerate(line.strip().split()):
                if answers[idx][0] == '+':
                    answers[idx][1] += int(number)
                elif answers[idx][0] == '*':
                    answers[idx][1] *= int(number)

    return answers


def part2(filename: str) -> List:
    '''
    We have to scan the whole file before we do any work because we need
    to construct columns since numbers and columnar.
    '''
    answers = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        columns = [[] for _ in range(len(lines[0]))]
        for line in lines:
            for col_idx, c in enumerate(line):
                columns[col_idx].append(c)


        numbers = []
        for col in columns:
            if col[-1] in ['+', '*']:
                operator = col[-1]
                numbers.append(int(''.join(col[:-1])))
            elif all(c in (' ', '\n') for c in col):
                if operator == '+':
                    answer = sum(numbers)
                elif operator == '*':
                    answer = functools.reduce(lambda x, y: x * y, numbers)
                answers.append( answer)
                numbers = []
            else:
                numbers.append(int(''.join(col)))
        

    return answers


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The input file with battery banks.")
    parser.add_argument(
        "--visualise", action="store_true", help="Show visualisation for part 2."
    )
    args = parser.parse_args()

    part1_start_time = time.time()
    answers = part1(args.filename)
    answer = functools.reduce(lambda x, y: x + y[1], answers, 0) 
    part1_end_time = time.time()

    print(f"part 1 answer: {answer} - time: {part1_end_time - part1_start_time:e}")

    #######################

    part2_start_time = time.time()
    answers = sum(part2(args.filename))
    part2_end_time = time.time()

    print(f"part 2 answer: {answers} - time: {part2_end_time - part2_start_time:e}")