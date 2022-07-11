import fileinput
import sys
from intcode import IntcodeMachine

class SantasSleigh:
    def __init__(self):
        self.machine = IntcodeMachine()
        self.machine.load_from_file('day25-input.txt')
        self.machine.run()

    def render(self):
        self.directions = []
        self.items = []
        chars = self.machine.read_outputs()
        for char in chars:
            if char == 10 or (char >= 32 and char < 127):
                sys.stdout.write(chr(char))
                if char == 45:
                    direction_or_item = True
                elif char == 10:
                    direction_or_item = False
            else:
                sys.stdout.write('[')
                for c in str(char):
                    sys.stdout.write(c)
                sys.stdout.write(']')
        sys.stdout.flush()
    
    def read_input(self):
        line = sys.stdin.readline()
        line.strip('\r')
        for char in line:
            self.machine.add_input(ord(char))

santasSleigh = SantasSleigh()
while not santasSleigh.machine.is_stopped():
    santasSleigh.render()
    santasSleigh.read_input()
    santasSleigh.machine.print_state()
santasSleigh.render()
