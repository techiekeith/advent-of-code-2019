import curses
import sys
from intcode import IntcodeMachine

class TractorBeamPlotter:
    def __init__(self):
        self.machine = IntcodeMachine()
        self.machine.load_from_file('day19-input.txt')

    def is_in_tractor_beam(self, x, y):
        self.machine.reset()
        self.machine.run()
        self.machine.add_input(x)
        self.machine.add_input(y)
        return self.machine.read_output() == '1'

    def plot_graph(self, size = 50, start_x = 0, start_y = 0):
        self.graph = []
        self.count = 0
        for y in range(0, size):
            self.graph.append([])
            for x in range(0, size):
                result = self.is_in_tractor_beam(start_x + x, start_y + y)
                self.count += 1 if result else 0
                self.graph[y].append('#' if result else '.')

    def render(self, window = None):
        for y in range(0, 50):
            line = ''.join(self.graph[y])
            if window == None:
                print line
            elif y < curses.LINES:
                window.addstr(y, 0, line[:curses.COLS])
        counter = ' [ Count: {} ] '.format(self.count)
        if window == None:
            print counter
        else:
            window.addstr(0, 10, counter)

    def find_square(self, size = 100):
        x = 0
        y = size - 1
        # find a suitable starting point
        while not self.is_in_tractor_beam(x + size - 1, y + 1 - size):
            y += 1
            while not self.is_in_tractor_beam(x, y):
                x += 1
        return [ x, y + 1 - size ]

def main(window):
    plotter = TractorBeamPlotter()
    plotter.plot_graph()
    plotter.render(window)
    if window != None:
        window.refresh()
        window.getkey()

if len(sys.argv) > 1 and sys.argv[1] == '-w':
    curses.wrapper(main)
else:
    main(None)

plotter = TractorBeamPlotter()
[x,y] = plotter.find_square()
print [x, y]
plotter.plot_graph(100, x, y)
plotter.render()