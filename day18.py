import fileinput
import re
from point import Point

dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]]

class Items:
    wall = 35
    entrance = 64
    door_base = 65
    key_base = 97
    max_keys = 26

class Route:
    path = []
    steps = 0
    source = ''
    keychain = ''
    keys_required = ''
    key_found = ''

    def __init__(self, path = [], source = '', keys_required = '', key_found = ''):
        if len(path) == 0:
            Route.path = []
        else:
            Route.path.append(path[-1])
        self.steps = len(path) - 1
        self.path = []
        self.path.extend(path)
        self.source = source
        self.keys_required = keys_required
        self.key_found = key_found

    def __str__(self):
        return 'source="{}" found="{}" required="{}" path=<{} steps>'.format(self.source, self.key_found, self.keys_required, self.steps)

    def __repr__(self):
        return 'Route({})'.format(str(self))

    def is_locked(self, path):
        locked = False
        for key in self.keys_required:
            if key not in path:
                locked = True
                break
        return locked

    def move(self, next_point, item):
        if next_point in Route.path or item == Items.wall:
            return None
        key_required = ''
        key_found = ''
        if item >= Items.door_base and item <= Items.door_base + Items.max_keys:
            key_required = chr(item + Items.key_base - Items.door_base)
        elif item >= Items.key_base and item <= Items.key_base + Items.max_keys:
            key_found = chr(item)
        path = []
        path.extend(self.path)
        path.append(next_point)
        return Route(path, self.source, self.keys_required + key_required, key_found)

class Maze:
    grid = []
    all_routes = {}
    visited_nodes = {}
    test_grid = False
    expected_start_x = -1
    expected_start_y = -1
    expected_total_keys = -1
    expected_result = -1
    start_point = Point()
    total_keys = -1
    last_key = ''

    def get_item_at(self, x, y):
        return ord(self.grid[y][x]) if y >= 0 and y < len(self.grid) and x >= 0 and x < len(self.grid[y]) else Items.wall
    
    def get_position_of(self, item):
        positions = []
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                if self.get_item_at(x, y) == item:
                    positions.append(Point(x, y))
        return positions

    def get_current_position(self):
        return self.get_position_of(Items.entrance)[0]

    def get_key_position(self, key_id):
        return self.get_position_of(Items.key_base + key_id)[0]

    def count_keys(self):
        total_keys = 0
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                item = self.get_item_at(x, y)
                if item >= Items.key_base and item < Items.key_base + Items.max_keys: # is a key
                    total_keys = total_keys + 1
        return total_keys

    def __init__(self, filename):
        self.grid = []
        self.all_routes = {}
        self.visited_nodes = {}
        self.test_grid = False
        self.expected_result = -1
        pattern = re.compile("^[0-9,]+$")
        for line in fileinput.input(files = (filename)):
            line = line.strip()
            if len(self.grid) == 0 and not self.test_grid and pattern.match(line):
                self.test_grid = True
                [ self.expected_start_x, self.expected_start_y, self.expected_total_keys, self.expected_result ] = list(map(int, line.split(',')))
                print 'Test maze {}: expecting start ({}, {}), {} keys, min {} steps'.format(filename, self.expected_start_x, self.expected_start_y, self.expected_total_keys, self.expected_result)
            else:
                self.grid.append(line)
        self.start_point = self.get_current_position()
        self.total_keys = self.count_keys()
        self.last_key = chr(Items.key_base + self.total_keys - 1)
    
    def verify(self):
        return self.test_grid and self.start_point.x == self.expected_start_x and self.start_point.y == self.expected_start_y and self.total_keys == self.expected_total_keys and self.expected_result > 0

    def add_routes(self, source, current_route):
        routes = []
        for next_step in range(0, 4):
            dx = dirs[next_step][0]
            dy = dirs[next_step][1]
            current_point = current_route.path[-1]
            next_point = current_point.add(dx, dy)
            item = self.get_item_at(next_point.x, next_point.y)
            # print "{} moving in dir {} to {}".format(current_route, next_step, next_point)
            next_route = current_route.move(next_point, item)
            if next_route != None:
                if next_route.key_found != '' and not self.all_routes[source].has_key(next_route.key_found):
                    # print 'Found key "{}" via route: {}'.format(next_route.key_found, next_route)
                    self.all_routes[source][next_route.key_found] = next_route
                routes.append(next_route)
        return routes

    def get_routes_between_keys(self, source, index = 0):
        print 'Finding routes from key {}[{}]'.format(source, index)
        Route()
        source_is_key = ord(source) != Items.entrance
        start_point = self.get_position_of(ord(source))[index]
        targets = self.total_keys
        if source_is_key:
            targets -= 1
        else:
            source = str(index)
        self.all_routes[source] = {}
        routes = [ Route([start_point], source) ]
        while len(routes) > 0 and len(self.all_routes[source]) < targets:
            new_routes = []
            for route in routes:
                new_routes.extend(self.add_routes(source, route))
            routes = new_routes

    def get_all_routes(self):
        start_points = self.get_position_of(Items.entrance)
        for index in range(0, len(start_points)):
            self.get_routes_between_keys(chr(Items.entrance), index)
        for key in range(0, self.total_keys):
            self.get_routes_between_keys(chr(Items.key_base + key))

    def plot_routes(self, path = '', steps = 0, last_sources = ['@']):
        next_routes_to_plot = []
        self.plot_count += 1
        if self.plot_count % 100000 == 0:
            print "[{}] path: {}; steps: {}, last sources: {}".format(self.plot_count, path, steps, last_sources)
        for source in last_sources:
            available_routes = self.all_routes[source]
            keys_to_check = list(filter(lambda next_key: next_key not in path and not available_routes[next_key].is_locked(path), available_routes))
            for next_key in sorted(keys_to_check, key=lambda next_key: available_routes[next_key].steps):
                # print "trying {} {}: {} steps; {}".format(last_sources, path, steps, next_key)
                next_path = path + next_key
                next_steps = steps + available_routes[next_key].steps
                source_index = last_sources.index(available_routes[next_key].source)
                next_sources = []
                next_sources.extend(last_sources)
                next_sources[source_index] = next_key
                all_keys = ''.join(sorted(path)) + ':' + ''.join(next_sources)
                if not self.visited_nodes.has_key(all_keys) or self.visited_nodes[all_keys][1] > next_steps:
                    self.visited_nodes[all_keys] = [ next_path, next_steps, next_sources ]
                    if len(next_path) < self.total_keys:
                        next_routes_to_plot.append([next_path, next_steps, next_sources])
        return next_routes_to_plot

    def walk(self):
        self.get_all_routes()
        # print "All routes: {}".format(self.all_routes)
        self.plot_count = 0
        start_sources = []
        for entrance in range(0, len(self.get_position_of(Items.entrance))):
            start_sources.append(str(entrance))
        next_routes_to_plot = self.plot_routes(last_sources = start_sources)
        while len(next_routes_to_plot) != 0:
            further_routes_to_plot = []
            for route_to_plot in next_routes_to_plot:
                further_routes_to_plot.extend(self.plot_routes(route_to_plot[0], route_to_plot[1], route_to_plot[2]))
            next_routes_to_plot = further_routes_to_plot
        # print "Visited nodes: {}".format(self.visited_nodes)
        all_keys = ''
        relevant_nodes = sorted(list(filter(lambda x: len(x.split(':')[0]) == self.total_keys - 1, self.visited_nodes)), key=lambda x: self.visited_nodes[x][1])
        return self.visited_nodes[relevant_nodes[0]] if len(relevant_nodes) > 0 else None

def run_part1_tests():
    for maze_id in range(0, 5):
        filename = 'day18-test-grid-{}.txt'.format(maze_id + 1)
        test_maze = Maze(filename)
        print 'Test maze loaded correctly: {}'.format(test_maze.verify())
        route = test_maze.walk()
        if route == None:
            print 'Did not find a route.'
        else:
            print 'Found route: {}'.format(str(route))
            print 'Expected route found: {}'.format(test_maze.expected_result == route[1])

def run_part1():
    filename = 'day18-input.txt'
    maze = Maze(filename)
    print 'Maze {}: start ({}, {}), {} keys'.format(filename, maze.start_point.x, maze.start_point.y, maze.total_keys)

    route = maze.walk()
    print 'Found route: {}'.format(str(route))

def run_part2_tests():
    for maze_id in range(0, 4):
        filename = 'day18-test-part2-grid-{}.txt'.format(maze_id + 1)
        test_maze = Maze(filename)
        print 'Test maze loaded correctly: {}'.format(test_maze.verify())
        route = test_maze.walk()
        if route == None:
            print 'Did not find a route.'
        else:
            print 'Found route: {}'.format(str(route))
            print 'Expected route found: {}'.format(test_maze.expected_result == route[1])

def run_part2():
    filename = 'day18-part2-input.txt'
    maze = Maze(filename)
    print 'Maze {}: start ({}, {}), {} keys'.format(filename, maze.start_point.x, maze.start_point.y, maze.total_keys)

    route = maze.walk()
    print 'Found route: {}'.format(str(route))

# run_part1_tests()
run_part1()
# run_part2_tests()
# run_part2()
