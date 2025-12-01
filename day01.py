import time


class Dial(object):
    def __init__(self, numbers):
        self.numbers = numbers
        self.old_password = 0
        self.new_password = 0
        self.position = 50

    def generate_movements(self, file: str):
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    yield (line[0], int(line[1:]))
    
    def _turn(self, movement: tuple[str, int]) -> None:
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

if __name__ == '__main__':
    dial = Dial(100)
    movements_generator = dial.generate_movements('day01_input01.txt')
    #movements_generator = dial.generate_movements('day01_test_input01.txt')
    
    start_time = time.time()
    dial.apply_movements(movements_generator)
    end_time = time.time()

    print(f"password: {dial.old_password}")
    print(f"new password: {dial.new_password}")
    print(f"solving time: {end_time - start_time:e} seconds")

