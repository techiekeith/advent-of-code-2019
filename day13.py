import curses
import time
from intcode import IntcodeMachine

class Game:
    tiles = ' /#=O'

    window = None
    machine = None
    score = 0
    paddle_x = 0
    ball_x = 0

    def __init__(self, window):
        self.window = window
        self.machine = IntcodeMachine()
        self.machine.load_from_file('day13-input.txt')
        self.machine.set_mem(0, 2)

    def render(self):
        outputs = self.machine.read_outputs()
        for output_index in range(0, len(outputs), 3):
            x = int(outputs[output_index])
            y = int(outputs[output_index + 1])
            tile = int(outputs[output_index + 2])
            if x == -1 and y == 0:
                self.score = tile
            else:
                self.window.addstr(y + 1, x, self.tiles[tile])
            if tile == 3:
                self.paddle_x = x
            if tile == 4:
                self.ball_x = x
        self.window.addstr(0, 0, 'Score: {}'.format(self.score))
        self.window.refresh()

    def run(self):
        self.machine.run()
        self.render()
        while not self.machine.is_stopped():
            self.machine.add_input(cmp(self.ball_x, self.paddle_x))
            self.render()
            time.sleep(0.05)

def main(window):
    window.clear()
    game = Game(window)
    game.run()
    window.getkey()

curses.wrapper(main)
