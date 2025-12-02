import math
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

def _number_of_digits(number):
    return math.floor(math.log10(number)) + 1

def generate_complex_invalid_ids(ranges):
    '''
    Instead of checking on all possible values in provided ranges, generate and check possible patterns.

    About 10x faster than find_complex_invalid_ids() above.
    '''
    invalid_ids = set()
    for start, stop in ranges:
        min_length = _number_of_digits(start)
        max_length = _number_of_digits(stop)

        windows = set()
        for length in range(min_length, max_length+1):
            windows.update(set([i for i in range(1, (length // 2)+1) if length % i == 0]))

        for window in windows:
            # All numbers with `window` digits that don't start with zero.
            candidates = (range(10**(window-1), (10**window)))
            min_multiplier = max(2, min_length // window) # Patterns have to repeat at least once
            max_multiplier = max_length // window
            for candidate in candidates:
                for multiplier in range(min_multiplier, max_multiplier+1):
                    num_digits = _number_of_digits(candidate)
                    power_of_10 = 10**num_digits
                    # This is the sum of a geometric series: 1 + power_of_10 + ...
                    # For a number c with d digits, repeating it m times is equivalent to c * (1 + 10^d + 10^(2d) + ... + 10^((m-1)d)).
                    geometric_sum = (power_of_10**multiplier - 1) // (power_of_10 - 1)
                    pattern = geometric_sum * candidate
                    if pattern in range(start, stop+1):
                        invalid_ids.add(pattern)

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

    start_generate_complex = time.time()
    generated_complex_invalid_ids = generate_complex_invalid_ids(ranges)
    end_generate_complex = time.time()


    print(f"part 1: {sum(simple_invalid_ids)} - time: {end_simple - start_simple:e} seconds")
    print(f"part 2: {sum(complex_invalid_ids)} - time: {end_complex - start_complex:e} seconds")
    print(f"part 3: {sum(generated_complex_invalid_ids)} - time: {end_generate_complex - start_generate_complex:e} seconds")

    
