import curses
import fileinput
import sys

empty = [ '.....', '.....', '..?..', '.....', '.....' ]
test1_input = [ '....#', '#..#.', '#..##', '..#..', '#....' ]
part1_input = [ '####.', '#....', '#..#.', '.#.#.', '##.##' ]
test2_input = [ '....#', '#..#.', '#.?##', '..#..', '#....' ]
part2_input = [ '####.', '#....', '#.?#.', '.#.#.', '##.##' ]

class ItsABugPlanet:
    def __init__(self, source_grid = empty, inner = None, outer = None):
        self.iteration = 0
        self.grid = []
        self.grid_height = len(source_grid)
        self.grid_width = len(source_grid[0])
        self.mid_y = (self.grid_height // 2)
        self.mid_x = (self.grid_width // 2)
        for y in range(0, self.grid_height):
            self.grid.append([])
            for x in range(0, self.grid_width):
                self.grid[y].append(1 if source_grid[y][x] == '#' else 0)
        self.past_ratings = [ self.rating() ]
        self.recursion = source_grid[self.mid_y][self.mid_x] == '?'
        self.inner = inner
        self.outer = outer
        self.next_grid_calculated = False

    def value_at(self, y, x):
        return self.grid[y][x] if y >= 0 and y < self.grid_height and x >= 0 and x < self.grid_width else 0

    def sum_of_values_at_row(self, y):
        bugs = 0
        for x in range(0, self.grid_width):
            bugs += self.grid[y][x]
        return bugs

    def sum_of_values_at_column(self, x):
        bugs = 0
        for y in range(0, self.grid_height):
            bugs += self.grid[y][x]
        return bugs
        
    def number_of_adjacent_bugs(self, y, x):
        bugs_outside = 0
        if self.recursion:
            if self.outer != None:
                if y == 0:
                    bugs_outside += self.outer.value_at(self.outer.mid_y - 1, self.outer.mid_x)
                elif y == self.grid_height - 1:
                    bugs_outside += self.outer.value_at(self.outer.mid_y + 1, self.outer.mid_x)
                if x == 0:
                    bugs_outside += self.outer.value_at(self.outer.mid_y, self.outer.mid_x - 1)
                elif x == self.grid_width - 1:
                    bugs_outside += self.outer.value_at(self.outer.mid_y, self.outer.mid_x + 1)
            if self.inner != None:
                if y == self.mid_y - 1 and x == self.mid_x:
                    bugs_outside += self.inner.sum_of_values_at_row(0)
                elif y == self.mid_y + 1 and x == self.mid_x:
                    bugs_outside += self.inner.sum_of_values_at_row(self.inner.grid_height - 1)
                elif x == self.mid_x - 1 and y == self.mid_y:
                    bugs_outside += self.inner.sum_of_values_at_column(0)
                elif x == self.mid_x + 1 and y == self.mid_y:
                    bugs_outside += self.inner.sum_of_values_at_column(self.inner.grid_width - 1)
        return bugs_outside + self.value_at(y - 1, x) + self.value_at(y, x - 1) + self.value_at(y, x + 1) + self.value_at(y + 1, x)

    def calculate_next_grid(self):
        if not self.next_grid_calculated:
            self.iteration += 1
            self.next_grid = []
            for y in range(0, self.grid_height):
                self.next_grid.append([])
                for x in range(0, self.grid_width):
                    bug = 0
                    if not self.recursion or y != self.mid_y or x != self.mid_x:
                        here = self.grid[y][x]
                        adjacent = self.number_of_adjacent_bugs(y, x)
                        bug = (1 if adjacent == 1 or adjacent == 2 else 0) if here == 0 else (1 if adjacent == 1 else 0)
                    self.next_grid[y].append(bug)
            self.next_grid_calculated = True
            if self.recursion:
                if self.inner == None:
                    has_inner_values = self.value_at(self.mid_y, self.mid_x - 1) + self.value_at(self.mid_y, self.mid_x + 1) + self.value_at(self.mid_y - 1, self.mid_x) + self.value_at(self.mid_y + 1, self.mid_x)
                    if has_inner_values:
                        self.inner = ItsABugPlanet(empty, None, self)
                if self.outer == None:
                    has_outer_values = self.sum_of_values_at_row(0) + self.sum_of_values_at_row(self.grid_height - 1) + self.sum_of_values_at_column(0) + self.sum_of_values_at_column(self.grid_width - 1)
                    if has_outer_values:
                        self.outer = ItsABugPlanet(empty, self, None)
                if self.inner != None:
                    self.inner.calculate_next_grid()
                if self.outer != None:
                    self.outer.calculate_next_grid()
    
    def tick(self):
        if self.next_grid_calculated:
            self.grid = self.next_grid
            self.past_ratings.append(self.rating())
            self.next_grid_calculated = False
            if self.inner != None:
                self.inner.tick()
            if self.outer != None:
                self.outer.tick()

    def rating(self):
        value = 0
        for y in range(0, self.grid_height):
            for x in range(0, self.grid_width):
                value = value << 1 | self.grid[y][x]
        return value
    
    def total_bugs_non_recursive(self):
        value = 0
        for y in range(0, self.grid_height):
            for x in range(0, self.grid_width):
                value += self.grid[y][x]
        return value

    def total_bugs_inner(self):
        return 0 if not self.recursion or self.inner == None else self.inner.total_bugs_non_recursive() + self.inner.total_bugs_inner()

    def total_bugs_outer(self):
        return 0 if not self.recursion or self.outer == None else self.outer.total_bugs_non_recursive() + self.outer.total_bugs_outer()

    def total_bugs(self):
        return self.total_bugs_non_recursive() + self.total_bugs_inner() + self.total_bugs_outer()

    def loop_detected(self):
        last = len(self.past_ratings) - 1
        return self.past_ratings[last] in self.past_ratings[:last]
    
    def render(self):
        rendered_grid = []
        for y in range(0, self.grid_height):
            line = ''
            for x in range(0, self.grid_width):
                line += '?' if self.recursion and y == self.mid_y and x == self.mid_x else '#' if self.grid[y][x] == 1 else '.'
            rendered_grid.append(line)
        return rendered_grid

def main(window = None):
    if window != None:
        window.clear()
    eris = ItsABugPlanet(part2_input)
    # Do some stuff
    loop = True
    while loop:
        iteration = 'Iteration {}, diversity rating {}, total {}           '.format(eris.iteration, eris.past_ratings[-1], eris.total_bugs())
        grid = eris.render()
        if window == None:
            print iteration
            print
            for line in grid:
                print line
            print
        else:
            window.addstr(0, 0, iteration)
            for line in range(0, len(grid)):
                window.addstr(line + 2, 7, grid[line])
            if eris.inner != None:
                inner_grid = eris.inner.render()
                for line in range(0, len(inner_grid)):
                    window.addstr(line + 2, 0, inner_grid[line])
            if eris.outer != None:
                outer_grid = eris.outer.render()
                for line in range(0, len(outer_grid)):
                    window.addstr(line + 2, 14, outer_grid[line])
            window.refresh()
            window.getkey()
            for line in range(0, len(grid)):
                window.addstr(line + 9, 7, grid[line])
            if eris.inner != None:
                for line in range(0, len(inner_grid)):
                    window.addstr(line + 9, 0, inner_grid[line])
            if eris.outer != None:
                for line in range(0, len(outer_grid)):
                    window.addstr(line + 9, 14, outer_grid[line])
        loop = not eris.loop_detected()
        eris.calculate_next_grid()
        eris.tick()

if len(sys.argv) > 1 and sys.argv[1] == '-w':
    curses.wrapper(main)
else:
    main()
