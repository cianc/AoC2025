import time
import os
import sys


class Dial(object):
    def __init__(self, numbers, visualise=False):
        self.numbers = numbers
        self.old_password = 0
        self.new_password = 0
        self.position = 50
        self._visualise = visualise

    def generate_movements(self, file: str):
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    yield (line[0], int(line[1:]))
    
    def _visualize_turn(self, movement):
        """Prints a single frame of the dial animation."""
        # Determine the correct clear command based on the OS
        os.system('clear')

        vis_width = 50
        # Scale the current position to the visualization width
        scaled_pos = int((self.position / self.numbers) * vis_width)
        scaled_pos = min(scaled_pos, vis_width - 1)

        dial_vis = ['-'] * vis_width
        dial_vis[scaled_pos] = '|'
        dial_vis_str = f"0 [{''.join(dial_vis)}] {self.numbers - 1}"
        
        direction, distance = movement
        move_str = f"Move: {direction}{distance}"
        
        print("--- Dial Visualization ---")
        print(dial_vis_str)
        print(f"Position: {self.position}/{self.numbers}")
        print(move_str)
        print(f"Old Password: {self.old_password}")
        print(f"New Password: {self.new_password}")
        print("--------------------------")
        
        # Pause to make the animation viewable
        time.sleep(0.05)

    def _turn(self, movement: tuple[str, int]) -> None:
        if self._visualise:
            self._visualize_turn(movement)

        direction, distance = movement

        if direction == 'R':
            new_pos_val = self.position + distance
            total_distance_from_zero = new_pos_val
            self.position = new_pos_val % self.numbers
        else:  # direction == 'L'
            # We have to `% self.numbers` to account for when current posistion is 0.
            # Technically the case for 'R' should be `(self.position - 0) % self.numbers`
            total_distance_from_zero = ((self.numbers - self.position) % self.numbers) + distance
            self.position = (self.position - distance) % self.numbers

        if self.position == 0:
            self.old_password += 1

        self.new_password += total_distance_from_zero // self.numbers
                
    def apply_movements(self, movements):
        for movement in movements:
            self._turn(movement)
        # Print a final blank line to move past the animation
        if self._visualise:
            print()  

if __name__ == '__main__':
    visualize_arg = len(sys.argv) > 1 and sys.argv[1] == '--visualise'

    dial = Dial(100, visualize_arg)
    movements_generator = dial.generate_movements('day01_input01.txt')
    #movements_generator = dial.generate_movements('day01_test_input01.txt')
    
    start_time = time.time()
    dial.apply_movements(movements_generator)
    end_time = time.time()

    print(f"password: {dial.old_password}")
    print(f"new password: {dial.new_password}")
    print(f"solving time: {end_time - start_time:e} seconds")

