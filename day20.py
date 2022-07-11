import curses
import fileinput
import re
import sys
from point import Point

class Items:
    space = 32
    wall = 35
    floor = 46
    portal_start = 64
    start_portal = 'AA'
    end_portal = 'ZZ'

class Maze:
    dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]]

    def get_source_grid_value_at(self, x, y):
        return ord(self.source_grid[y][x]) if x >= 0 and y >= 0 and y < len(self.source_grid) and x < len(self.source_grid[y]) else Items.space

    def get_grid_value_at(self, point):
        return self.grid[point.y][point.x] if point.x >= 0 and point.y >= 0 and point.y < len(self.grid) and point.x < len(self.grid[point.y]) else Items.space

    def is_visited(self, point):
        return point.x >= 0 and point.y >= 0 and point.y < len(self.visited) and point.x < len(self.visited[point.y]) and self.visited[point.y][point.x]

    def visit(self, point):
        while point.y >= len(self.visited):
            self.visited.append([])
        while point.x >= len(self.visited[point.y]):
            self.visited[point.y].append(False)
        self.visited[point.y][point.x] = True

    def get_portals(self):
        self.portals_by_position = {}
        self.portals_by_name = {}
        for i in range(0, len(self.portal_chars)):
            [ this_x, this_y, this_char ] = self.portal_chars[i]
            for [ other_x, other_y, other_char ] in self.portal_chars[i+1:]:
                [ x, y ] = [ None, None ]
                if this_x == other_x and other_y - this_y == 1:
                    adjacent_to_first = (self.get_source_grid_value_at(this_x, this_y - 1)) == Items.floor
                    x = this_x
                    y = this_y if adjacent_to_first else other_y
                    next_x = this_x
                    next_y = this_y - 1 if adjacent_to_first else other_y + 1
                elif this_y == other_y and other_x - this_x == 1:
                    adjacent_to_first = (self.get_source_grid_value_at(this_x - 1, this_y)) == Items.floor
                    x = this_x if adjacent_to_first else other_x
                    y = this_y
                    next_x = this_x - 1 if adjacent_to_first else other_x + 1
                    next_y = this_y
                if x != None and y != None:
                    pos = Point(x, y)
                    next_pos = Point(next_x, next_y)
                    portal_name = chr(this_char) + chr(other_char)
                    if not self.portals_by_name.has_key(portal_name):
                        self.portals_by_name[portal_name] = []
                    self.portals_by_name[portal_name].append([pos, next_pos])
                    if portal_name == Items.start_portal:
                        self.start_portal = next_pos
                    elif portal_name == Items.end_portal:
                        self.end_portal = next_pos
                    else:
                        self.portals_by_position[pos] = portal_name

    def decode_grid(self):
        self.grid = []
        self.portal_chars = []
        max_rows = len(self.source_grid)
        max_columns = 0
        for row in range(0, max_rows):
            columns = len(self.source_grid[row])
            if max_columns < columns:
                max_columns = columns
            for column in range(0, columns):
                char = self.get_source_grid_value_at(column, row)
                if char > Items.portal_start:
                    self.portal_chars.append([column, row, char])
        self.get_portals()
        for row in range(0, max_rows):
            self.grid.append([])
            columns = len(self.source_grid[row])
            for column in range(0, max_columns):
                char = self.get_source_grid_value_at(column, row)
                if char > Items.portal_start:
                    pos = Point(column, row)
                    char = self.portals_by_position[pos] if self.portals_by_position.has_key(pos) else Items.space
                self.grid[row].append(char)
            print self.grid[row]

    def load_grid(self, filename):
        self.source_grid = []
        self.test_grid = False
        self.start_portal_x = 0
        self.start_portal_y = 0
        self.end_portal_x = 0
        self.end_portal_y = 0
        self.expected_result = 0
        pattern = re.compile("^[0-9,]+$")
        for line in fileinput.input(files = (filename)):
            line = line.rstrip()
            if len(self.source_grid) == 0 and not self.test_grid and pattern.match(line):
                self.test_grid = True
                [ self.start_portal_x, self.start_portal_y, self.end_portal_x, self.end_portal_y, self.expected_result ] = list(map(int, line.split(',')))
            else:
                self.source_grid.append(line)
        self.decode_grid()

    def add_points(self, point):
        points = []
        self.visit(point)
        # print "Visiting {} <{}>".format(point, point.moves)
        for next_step in range(0, 4):
            dx = Maze.dirs[next_step][0]
            dy = Maze.dirs[next_step][1]
            next_point = point.add(dx, dy)
            if next_point == self.end_portal:
                # print "Found end portal at {}".format(next_point)
                return [ next_point ]
            if not self.is_visited(next_point):
                item = self.get_grid_value_at(next_point)
                if item != Items.wall and item != Items.space:
                    if item == Items.floor:
                        points.append(next_point)
                    elif self.portals_by_position.has_key(next_point):
                        portal_name = self.portals_by_position[next_point]
                        # print "Found portal {} at {}".format(self.portals_by_position[next_point], next_point)
                        for [pos, next_pos] in self.portals_by_name[portal_name]:
                            if next_point.x != pos.x or next_point.y != pos.y:
                                # print "Other end of {} is at {}".format(next_point, next_pos)
                                teleport = Point(next_pos.x, next_pos.y, next_point.moves)
                                points.append(teleport)
        return points

    def walk(self):
        self.visited = []
        points = [ self.start_portal ]
        while len(points) > 0:
            next_points = []
            for point in points:
                points_to_add = self.add_points(point)
                if len(points_to_add) > 0:
                    next_point = points_to_add[0]
                    if next_point == self.end_portal:
                        return next_point
                    next_points.extend(points_to_add)
            points = next_points
        return None

    def test(self):
        if self.test_grid:
            start_portal_position_correct = self.start_portal_x == self.start_portal.x and self.start_portal_y == self.start_portal.y
            end_portal_position_correct = self.end_portal_x == self.end_portal.x and self.end_portal_y == self.end_portal.y
            expected_result_correct = self.expected_result == self.walk().moves
            print "Start ({},{}): {}".format(self.start_portal_x, self.start_portal_y, start_portal_position_correct)
            print "End ({},{}): {}".format(self.end_portal_x, self.end_portal_y, end_portal_position_correct)
            print "Found exit in {} moves: {}".format(self.expected_result, expected_result_correct)
        else:
            print "Not a test maze!"

    def __init__(self, filename):
        self.load_grid(filename)

Maze('day20-test-grid-1.txt').test()
Maze('day20-test-grid-2.txt').test()

maze = Maze('day20-input.txt')
print maze.walk().moves
