import argparse
import copy
import itertools
import scipy
import time

from typing import List, Tuple

class Machine(object):
    def __init__(self, lights, buttons, jolts):
        self.lights = self.bitmap_int_from_bitmap_list(lights)
        self.buttons = self.bitmap_buttons(buttons)
        self.buttons_list = buttons
        self.jolts = jolts

    def __repr__(self):
        return f"lights: {self.lights} ({self.lights:b}), buttons: {self.buttons_list} ({', '.join(f'{b:b}' for b in self.buttons)}), jolts: {self.jolts}"
        
    def bitmap_int_from_bitmap_list(self, lights: List[int]) -> int:
        output = 0
        for idx, light in enumerate(lights):
            if light:
                output += 1 << idx
        return output
    
    def bitmap_buttons(self, buttons_list: List[List[int]]) -> int:
        output = []

        for buttons in buttons_list:
            binary_list = []
            for idx in range(max(buttons)+1):
                if idx in buttons:
                    binary_list.append(1)
                else:
                    binary_list.append(0)

            binary_list = list(binary_list)
            output.append(self.bitmap_int_from_bitmap_list(binary_list))

        return(output)

    
def parse_input(filename: str) -> List[Machine]:
    machines = []

    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]  
        for line in lines:
            parts = line.split()
            
            # eg: [1, 0, 1, 1, 0]
            lights = [int(c == '#') for c in parts[0].strip('[]')]

            buttons = [b.strip('()').split(',') for b in parts[1:-1]]
            # eg: [[0,1, 7, 5], [7, 1, 0]]
            buttons = [list(map(lambda x: int(x), b)) for b in buttons]

            # eg [1, 3, 5, 7]
            jolts = [int(c) for c in parts[-1].strip('{}').split(',')]

            machines.append(Machine(lights, buttons, jolts))

    return machines


def apply_buttons_to_lights(bitmap_buttons: List[int], lights: int):
    for bitmap_button in bitmap_buttons:
        lights = lights ^ bitmap_button
    return lights

def part1(machines: List[Machine]) -> int:
    button_press_count_sum = 0

    for machine in machines:
        button_presses = 1
        solved = False
        while not solved:
            for buttons in itertools.combinations_with_replacement(machine.buttons, button_presses):
                result_lights = apply_buttons_to_lights(buttons, 0)
                if result_lights == machine.lights:
                    button_press_count_sum += button_presses
                    solved = True
                    break

            button_presses += 1

    return button_press_count_sum

def buttons_set_jolts(bitmap_buttons: List[int], target_jolts: List[int], jolts_set: set) -> bool:
    bitmap_button_mask = 0
    for button in bitmap_buttons:
        bitmap_button_mask |= button

    for jolt_idx in range(len(target_jolts)):
        if not bitmap_button_mask & (1 << jolt_idx):
            return False
        button_sum = 0
        for button in bitmap_buttons:
            if button & (1 << jolt_idx):
                button_sum += 1
        if button_sum != target_jolts[jolt_idx]:
            return False

    return True
    

def part2(machines: List[Machine]) -> int:
    button_press_count_sum = 0

    machine_idx = 1
    for machine in machines:
        print(f"{machine_idx}/{len(machines)}")
        # Need at least as many button presses as the max jolt value to sum to the max jolt value.
        button_presses = max(machine.jolts)
        solved = False
        jolts_set = set(machine.jolts)
        while not solved:
            for buttons in itertools.combinations_with_replacement(machine.buttons, button_presses):
                if buttons_set_jolts(buttons, machine.jolts, jolts_set):
                    button_press_count_sum += button_presses
                    solved = True
                    break

            button_presses += 1
        machine_idx += 1

    return button_press_count_sum

def _recurse_part2a(buttons: List[int], all_buttons: List[List[int]], jolts: List[int], target_jolts: List[int]):
    print(f"buttons: {buttons}, jolts: {jolts}, target_jolts: {target_jolts}")
    _jolts = copy.deepcopy(jolts)
    for button in buttons:
        _jolts[button] += 1

    if _jolts == target_jolts:
        return 1
    if any(j > tj for j, tj in zip(_jolts, target_jolts)):
        print(f"FAILED: jolts: {_jolts}, target_jolts: {target_jolts}")
        return None
    
    for buttons in all_buttons:
        result = _recurse_part2a(buttons, all_buttons, _jolts, target_jolts)
        if result:
            print(f"result: {result}")
            return result+1

def _bfs_part2a(all_buttons: List[List[int]], target_jolts: List[int]):
    button_press_count = 0
    branches = [[0] * len(target_jolts)]

    while True:
        #time.sleep(1)
        #print("====================")
        #print(f"branches: {branches}")
        #print("====================")

        new_branches = []
        for jolts in branches:
            if jolts == target_jolts:
               return button_press_count
            if any(j > tj for j, tj in zip(jolts, target_jolts)):
               continue
            for buttons in all_buttons:
                #print(f"button_press_count: {button_press_count}")
                new_jolts = copy.deepcopy(jolts)
                for button in buttons:
                    new_jolts[button] += 1
                new_branches.append(new_jolts)
                #print(f"new_branches: {new_branches}")
        branches = new_branches
        button_press_count += 1
        print(f"button_press_count: {button_press_count}")
        
       
    return button_press_count


def part2a(machines: List[Machine]) -> int:
    button_press_count_sum = 0

    for machine in machines:
        result = _bfs_part2a(machine.buttons_list, machine.jolts)
        button_press_count_sum += result

    return button_press_count_sum


def part2_linprog(machines: List[Machine]) -> int:
    '''
    Use scipy linear programming module, see 
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html

    How we use it:
    1. Create a set of constraints. Each value in machine.jolt, is a sum of button
       pushes. Eg: if jolts are [3,5], that requires 3 pushes of any buttons that
       toggles the first counter and 5 pushes of any buttons that toggles the second
       counter. If we have two buttons (0,1) and (1,) we could write these constraints
       as: x0 = 3; x0 + x1 = 5, where xn is the number of times a button is pushed.
       These can be written as an equality contstraint matrix A=[[1,0],[1,1]] and an
       equality constraint vector b=[3,5].
    2. Create a vector for the function we want to minimise. In our case it's the
        sum of the button presses, eg: x0+x1, or c=[1,1]
    3. Create the bounds for our answers, we just want them to be positive so it's
       (0, None) for each button count, or ((0, None), (0, None)) in our example.
    4. We feed the above into scipy.optimize.linprod, setting `integrality=1` becase
       we only want integer solutions.
    '''
    button_press_count_sum = 0

    machine_idx = 1
    for machine in machines:
        print(f"{machine_idx}/{len(machines)}")

        A = []
        for jolt_idx, _ in enumerate(machine.jolts):
            A.append([int(jolt_idx in button) for button in machine.buttons_list])
        b = machine.jolts
        c = [1 for _ in machine.buttons_list]
        bounds = [(0, None) for _ in machine.buttons_list]

        res=scipy.optimize.linprog(c, A_eq=A, b_eq=b, bounds=bounds, integrality=1)

        print(f"res: {res.x}")

        button_press_count_sum += int(sum(res.x))

        machine_idx += 1

    return button_press_count_sum
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="The input file with battery banks.")
    parser.add_argument('--visualise', action='store_true', help="Show visualisation for part 2.")
    args = parser.parse_args()

    machines = parse_input(args.filename)
    for machine in machines:
        print(machine)

    part1_start_time = time.time()
    answer = part1(machines)
    part1_end_time = time.time()

    print(f"part 1 answer: {answer} - time: {part1_end_time - part1_start_time:e} seconds")
    
    ###################

    part2_start_time = time.time()
    answer = part2_linprog(machines)
    part2_end_time = time.time()

    print(f"part 2 answer: {answer} - time: {part2_end_time - part2_start_time:e} seconds")