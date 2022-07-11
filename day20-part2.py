import curses
import fileinput
import re
import sys
from point3d import Point3D

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
        return point.x >= 0 and point.y >= 0 and point.z >= 0 and point.z < len(self.visited) and point.y < len(self.visited[point.z]) and point.x < len(self.visited[point.z][point.y]) and self.visited[point.z][point.y][point.x]

    def visit(self, point):
        while point.z >= len(self.visited):
            self.visited.append([])
        while point.y >= len(self.visited[point.z]):
            self.visited[point.z].append([])
        while point.x >= len(self.visited[point.z][point.y]):
            self.visited[point.z][point.y].append(False)
        self.visited[point.z][point.y][point.x] = True

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
                    pos = Point3D(x, y)
                    next_pos = Point3D(next_x, next_y)
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
        # print self.portals_by_position
        # print self.portals_by_name
        for row in range(0, max_rows):
            self.grid.append([])
            columns = len(self.source_grid[row])
            for column in range(0, max_columns):
                char = self.get_source_grid_value_at(column, row)
                if char > Items.portal_start:
                    pos = Point3D(column, row)
                    char = self.portals_by_position[pos] if self.portals_by_position.has_key(pos) else Items.space
                self.grid[row].append(char)

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
                [ self.start_portal_x, self.start_portal_y, self.end_portal_x, self.end_portal_y, self.expected_part1_result, self.expected_part2_result ] = list(map(int, line.split(',')))
            else:
                self.source_grid.append(line)
        self.decode_grid()

    def add_points(self, point):
        points = []
        if self.is_visited(point):
            return points
        self.visit(point)
        # print "Visiting {} <{}>".format(point, point.moves)
        for next_step in range(0, 4):
            dx = Maze.dirs[next_step][0]
            dy = Maze.dirs[next_step][1]
            next_point = point.add(dx, dy)
            flat_next_point = Point3D(next_point.x, next_point.y, 0, next_point.moves)
            if next_point == self.end_portal:
                # print "Found end portal at {}".format(next_point)
                return [ next_point ]
            if not self.is_visited(next_point):
                item = self.get_grid_value_at(next_point)
                if item != Items.wall and item != Items.space:
                    if item == Items.floor:
                        points.append(next_point)
                    elif self.portals_by_position.has_key(flat_next_point):
                        is_outer_portal = next_point.x < 2 or next_point.y < 2 or next_point.x >= len(self.source_grid[next_point.y]) - 2 or next_point.y >= len(self.source_grid) - 2
                        next_z = next_point.z + (-1 if is_outer_portal else 1)
                        portal_name = self.portals_by_position[flat_next_point]
                        if next_z >= 0 and portal_name != Items.start_portal and portal_name != Items.end_portal:
                            # print "Found portal {} at {}".format(portal_name, next_point)
                            for [pos, next_pos] in self.portals_by_name[portal_name]:
                                if next_point.x != pos.x or next_point.y != pos.y:
                                    teleport = Point3D(next_pos.x, next_pos.y, next_z, next_point.moves)
                                    # print "Other end of {} is at {}".format(next_point, teleport)
                                    points.append(teleport)
        return points

    def walk(self):
        self.visited = []
        points = [ self.start_portal ]
        count = 0
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
            count += 1
            print "{}: {} paths open".format(count, len(points))
        return None

    def test(self):
        if self.test_grid:
            start_portal_position_correct = self.start_portal_x == self.start_portal.x and self.start_portal_y == self.start_portal.y
            end_portal_position_correct = self.end_portal_x == self.end_portal.x and self.end_portal_y == self.end_portal.y
            result = self.walk()
            expected_result_correct = self.expected_part2_result == (0 if result is None else result.moves)
            print "Start ({},{}): {}".format(self.start_portal_x, self.start_portal_y, start_portal_position_correct)
            print "End ({},{}): {}".format(self.end_portal_x, self.end_portal_y, end_portal_position_correct)
            print "Found exit in {} moves: {}".format(self.expected_part2_result, expected_result_correct)
        else:
            print "Not a test maze!"

    def __init__(self, filename):
        self.load_grid(filename)

# Maze('day20-test-grid-1.txt').test()
# Maze('day20-test-grid-2.txt').test()
# Maze('day20-test-grid-3.txt').test()

maze = Maze('day20-input.txt')
print maze.walk().moves
