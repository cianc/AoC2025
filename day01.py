class Dial(object):
    def __init__(self, numbers):
        self.numbers = numbers
        self.old_password = 0
        self.new_password = 0
        self.position = 50
        self.movements = []

    def parse_input(self, file: str) -> None:
        with open(file, 'r') as f:
            lines = f.readlines()
        lines = [l.strip() for l in lines]
        self.movements = [(l[0], int(l[1:])) for l in lines]
    
    def _turn(self, movement: tuple[str, int]) -> None:
        direction, distance = movement

        if direction == 'R':
            total_distance_from_zero = self.position + distance
            self.position = (self.position + distance) % self.numbers
        elif direction == 'L':
            # We have to `% self.numbers` to account for when current posistion is 0.
            # Technically the case for 'R' should be `(self.position - 0) % self.numbers`
            total_distance_from_zero = ((self.numbers - self.position) % self.numbers) + distance
            self.position = (self.position - distance) % self.numbers

        if self.position == 0:
            self.old_password += 1

        self.new_password += total_distance_from_zero // self.numbers
                
    def apply_movements(self):
        for movement in self.movements:
            self._turn(movement)  

if __name__ == '__main__':
    dial = Dial(100)
    dial.parse_input('day01_input01.txt')
    #dial.parse_input('day01_test_input01.txt')
    dial.apply_movements()
    print(f"password: {dial.old_password}")
    print(f"new password: {dial.new_password}")

