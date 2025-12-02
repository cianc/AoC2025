import re
import sys
import time

def parse_ranges(file: str) -> list[list[int, int]]:
    ranges = []
    with open(file, 'r') as f:
        range_strings = [r.strip() for r in f.read().split(',')]

    for r in range_strings:
        ranges.append([int(s) for s in r.split('-')])

    return ranges

def find_simple_invalid_ids(ranges):
    invalid_ids = []
    for start, stop in ranges:
        for number in range(start, stop+1):
            str_number = str(number)
            len_number = len(str_number)
            if str_number[:len_number // 2] == str_number[len_number // 2:]:
                invalid_ids.append(number)

    return invalid_ids

def find_complex_invalid_ids(ranges):
    invalid_ids = []
    for start, stop in ranges:
        for number in range(start, stop+1):
            str_number = str(number)
            len_number = len(str_number)
            # Pattern has to repeat at least twice, so stop looking half way through the string
            windows = [(i, len_number // i) for i in range(1, (len_number // 2)+1) if len_number % i == 0]
            for window_size, window_multiplier in windows:
                if str_number[:window_size] * window_multiplier == str_number:
                    invalid_ids.append(number)
                    break

    return invalid_ids

    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        raise ValueError('Missing filename argument.')

    ranges = parse_ranges(filename)
    start_simple = time.time()
    simple_invalid_ids = find_simple_invalid_ids(ranges)
    end_simple = time.time()

    start_complex = time.time()
    complex_invalid_ids = find_complex_invalid_ids(ranges)
    end_complex = time.time()


    print(f"part 1: {sum(simple_invalid_ids)} - time: {end_simple - start_simple:e} seconds")
    print(f"part 2: {sum(complex_invalid_ids)} - time: {end_complex - start_complex:e} seconds")
    
