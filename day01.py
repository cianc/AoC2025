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
        full_rotations = distance // self.numbers
        remaining_clicks = distance % self.numbers
        zero_clicks = full_rotations

        if direction == 'R':
            new_position = (self.position + remaining_clicks) % self.numbers
            if remaining_clicks >= (self.numbers - self.position):
                zero_clicks += 1
        elif direction == 'L':
            new_position = (self.position - remaining_clicks) % self.numbers
            if remaining_clicks >= self.position and self.position != 0:
                zero_clicks += 1
        
        self.position = new_position
        if self.position == 0:
            self.old_password += 1
        self.new_password += zero_clicks

                
    def apply_movements(self):
        for movement in self.movements:
            self._turn(movement)  

if __name__ == '__main__':
    dial = Dial(100)
    dial.parse_input('day01_input01.txt')
    dial.apply_movements()
    print(f"password: {dial.old_password}")
    print(f"new password: {dial.new_password}")

