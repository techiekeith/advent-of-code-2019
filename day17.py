import curses
import fileinput
import re
import sys
from intcode import IntcodeMachine
from point import Point

class ShipExterior:
    code = ''
    grid = []
    intersections = []
    alignment_parameters = []
    machine = None
    droid = Point()
    droid_dir = 0
    moves = [ [0, -1], [1, 0], [0, 1], [-1, 0] ]

    def get_machine(self):
        return self.machine
    
    def wake_up_droid(self):
        self.machine.reset()
        self.machine.load_code(self.code)
        self.machine.set_mem(0, 2)
        self.machine.run()

    def load_grid_from_intcode_program(self, code):
        self.code = code
        self.grid = []
        self.machine = IntcodeMachine()
        self.machine.load_code(code)
        self.machine.run()
        grid_values = self.machine.read_outputs()
        line = ''
        for grid_value in grid_values:
            char = chr(int(grid_value))
            if char == '\n':
                self.grid.append(line)
                line = ''
            else:
                line = line + char
        if line != '':
            self.grid.append(line)

    def get_grid_position(self, x, y):
        return self.grid[y][x] if y >= 0 and y < len(self.grid) and x >= 0 and x < len(self.grid[y]) else '.'

    def mark_points_of_interest(self):
        self.intersections = []
        self.alignment_parameters = []
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                west = self.get_grid_position(x - 1, y)
                east = self.get_grid_position(x + 1, y)
                south = self.get_grid_position(x, y + 1)
                north = self.get_grid_position(x, y - 1)
                here = self.get_grid_position(x, y)
                if west == '#' and east == '#' and south == '#' and north == '#' and here == '#':
                    self.grid[y] = self.grid[y][:x] + 'O' + self.grid[y][x+1:]
                    self.intersections.append(Point(x, y))
                    self.alignment_parameters.append(x * y)
                if here == '^' or here == '>' or here == 'v' or here == '<':
                    self.droid = Point(x, y)
                    self.droid_dir = '^>v<'.index(here)

    def calculate_raw_path(self):
        # print "Start at {} facing dir {}".format(self.droid, self.droid_dir)
        path = []
        while True:
            count = 0
            left = (self.droid_dir - 1) % 4
            left_point = self.droid.add(self.moves[left][0], self.moves[left][1])
            # print "left is {}".format(left_point)
            if self.get_grid_position(left_point.x, left_point.y) != '.':
                # print "going left..."
                dir_char = 'L'
                ahead_point = left_point
                self.droid_dir = left
            else:
                right = (self.droid_dir + 1) % 4
                right_point = self.droid.add(self.moves[right][0], self.moves[right][1])
                # print "right is {}".format(right_point)
                if self.get_grid_position(right_point.x, right_point.y) != '.':
                    # print "going right..."
                    dir_char = 'R'
                    ahead_point = right_point
                    self.droid_dir = right
                else:
                    return path
            count = 0
            while self.get_grid_position(ahead_point.x, ahead_point.y) != '.':
                # print "going ahead to {}...".format(ahead_point)
                self.droid = ahead_point
                count = count + 1
                ahead_point = self.droid.add(self.moves[self.droid_dir][0], self.moves[self.droid_dir][1])
            path.append(dir_char)
            path.append(str(count))

    def get_intersections(self):
        return self.intersections

    def get_alignment_parameters(self):
        return self.alignment_parameters

    def __str__(self):
        return '\n'.join(self.grid)

    def __init__(self, filename):
        lines = []
        for line in fileinput.input(files=(filename)):
            lines.append(line.strip())
        pattern = re.compile("^[0-9,-]+$")
        if (pattern.match(lines[0])):
            self.load_grid_from_intcode_program(lines[0])
        else:
            self.grid = lines
        self.mark_points_of_interest()
    
    def render(self, window):
        if window == None:
            return
        max_y = len(self.grid)
        max_x = len(self.grid[0])
        if max_y > curses.LINES:
            max_y = curses.LINES
        if max_x > curses.COLS:
            max_x = curses.COLS
        for y in range(0, max_y):
            line = self.grid[y][:max_x]
            window.addstr(y, 0, line)
        window.addstr(0, 0, '[ {} ]'.format(sum(self.alignment_parameters)))
        window.refresh()
    
def is_valid_sub_path(path):
    length = 0
    if path[0] != 'L' and path[0] != 'R':
        return False
    if path[len(path) - 1] == 'L' or path[len(path) - 1] == 'R':
        return False
    for element in path:
        if element == 'A' or element == 'B' or element == 'C':
            return False
        if length != 0:
            length = length + 1
        length = length + len(element)
    return True if length < 20 else False

def replace_longest_repeating_pattern(source, replacement):
    pattern = []
    new_list = []
    index = -1
    found_length = 0
    for sequence_length in range(len(source) / 2, 0, -1):
        for first_pos in range(0, len(source) - sequence_length * 2):
            if is_valid_sub_path(source[first_pos:first_pos+sequence_length]):
                for second_pos in range(first_pos + sequence_length, len(source) - sequence_length):
                    if source[first_pos:first_pos+sequence_length] == source[second_pos:second_pos+sequence_length]:
                        print "Found repeating pattern {} @ indexes {} and {}".format(source[first_pos:first_pos+sequence_length], first_pos, second_pos)
                        pattern = source[first_pos:first_pos+sequence_length]
                        index = first_pos
                        found_length = sequence_length
                        break
            if index >= 0:
                break
        if index >= 0:
            break
    last = 0
    if index >= 0:
        while index < len(source):
            if pattern == source[index:index+found_length]:
                if index > last:
                    new_list.extend(source[last:index])
                new_list.append(replacement)
                index = index + found_length
                last = index
            else:
                index = index + 1
    new_list.extend(source[last:])
    return [ pattern, new_list ]

def main(window):
    if window != None:
        window.clear()
    ext = ShipExterior('day17-input.txt')
    # Do stuff here
    ext.render(window)

    # Calculate paths
    path = ext.calculate_raw_path()
    if window == None:
        print 'Raw path: {}'.format(path)
    [ program_a, path ] = replace_longest_repeating_pattern(path, 'A')
    [ program_b, path ] = replace_longest_repeating_pattern(path, 'B')
    [ program_c, path ] = replace_longest_repeating_pattern(path, 'C')
    if window == None:
        print 'Main program: {}'.format(path)
        print 'Path A: {}'.format(program_a)
        print 'Path B: {}'.format(program_b)
        print 'Path C: {}'.format(program_c)

    # Feed paths to machine
    input_lines = ''
    for line in [ path, program_a, program_b, program_c, 'n' ]:
        input_lines = input_lines + ','.join(line) + '\n'
    if window == None:
        print input_lines
    ext.wake_up_droid()
    for code in input_lines:
        outputs = ext.get_machine().read_outputs()
        print outputs
        ext.get_machine().add_input(ord(code))
    dust_collected = ext.get_machine().read_outputs()
    if window == None:
        print 'Dust collected: {}'.format(dust_collected[len(dust_collected) - 1])
    else:
        window.addstr(42, 0, 'Dust collected: {}'.format(dust_collected))
    if window != None:
        window.getkey()

def run_tests():
    ext1 = ShipExterior('day17-test-grid.txt')
    points = ext1.get_intersections()
    point1_correct = points[0] == Point(2,2)
    print "Point 1 (2,2) is {}: {}".format(points[0], point1_correct)
    point2_correct = points[1] == Point(2,4)
    print "Point 2 (2,4) is {}: {}".format(points[1], point2_correct)
    point3_correct = points[2] == Point(6,4)
    print "Point 3 (6,4) is {}: {}".format(points[2], point3_correct)
    point4_correct = points[3] == Point(10,4)
    print "Point 4 (10,4) is {}: {}".format(points[3], point4_correct)
    params = ext1.get_alignment_parameters()
    print "Param 1, 4 is {}: {}".format(params[0], params[0] == 4)
    print "Param 2, 8 is {}: {}".format(params[1], params[1] == 8)
    print "Param 3, 24 is {}: {}".format(params[2], params[2] == 24)
    print "Param 4, 40 is {}: {}".format(params[3], params[3] == 40)
    total = sum(params)
    print "Total, 76 is {}: {}".format(total, total == 76)
    if (point1_correct and point2_correct and point3_correct and point4_correct
    and params[0] == 4 and params[1] == 8 and params[2] == 24 and params[3] == 40
    and total == 76):
        print "All tests passed."
    else:
        print "There were test failures."
        exit(1)
    ext1.grid[6] = ext1.grid[6][:10] + '<' + ext1.grid[6][11:]
    ext1.droid_dir = 3
    print "Raw path: {}".format(ext1.calculate_raw_path())

def run_replacement_tests():
    path = [ 'R4', 'R6', 'R4', 'R6' ]
    [ program, path ] = replace_longest_repeating_pattern(path, 'A')
    print program
    print path

run_tests()
run_replacement_tests()

if len(sys.argv) > 1 and sys.argv[1] == '-w':
    curses.wrapper(main)
else:
    main(None)
