import fileinput
import re
from point import Point

dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]]

class Route:
    point = 0
    path = ''
    keychain = ''
    keys_required = ''
    points = []
    dead = False

    def __init__(self, point, path = '', keychain = '', keys_required = '', points = []):
        self.point = point
        self.path = path
        self.keychain = keychain
        self.keys_required = keys_required
        self.points = []
        self.points.extend(points)
        self.points.append(point)
    
    def __str__(self):
        return 'path=<{}> keychain=<{}> keys_required=<{}>'.format(self.path, self.keychain, self.keys_required)

    def has_visited(self, point):
        return point in self.points[:-1]

    def has_all_keys(self, keychain):
        for key in keychain:
            if not key in self.keychain:
                return False
        return True

    def update(self, step, item):
        new_key = ''
        keys_required = self.keys_required
        next_point = Point(self.point.x + dirs[step][0], self.point.y + dirs[step][1])
        if next_point in self.points:
            return None # Been here already since entering or collecting last key
        if item == 35: # Wall
            return None # can't go that way
        if item >= 65 and item <= 90: # Door
            key_to_find = chr(item + 32)
            if key_to_find in self.keychain:
                keys_required += key_to_find
            else:
                return None # need key to unlock door
        elif item >= 97 and item <= 122 and chr(item) not in self.keychain: # Key
            new_key = chr(item) # collect key
        # Anything else is not an obstacle or of interest
        return Route(next_point, self.path + str(step), self.keychain + new_key, keys_required, self.points)

class Maze:
    grid = []
    test_grid = False
    expected_start_x = -1
    expected_start_y = -1
    expected_total_keys = -1
    expected_result = -1
    start_point = Point()
    total_keys = -1

    def get_item_at(self, x, y):
        return ord(self.grid[y][x]) if y >= 0 and y < len(self.grid) and x >= 0 and x < len(self.grid[y]) else 35 # wall
    
    def get_position_of(self, item):
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                if self.get_item_at(x, y) == item:
                    return Point(x, y)
        return None

    def get_current_position(self):
        return self.get_position_of(64)

    def get_key_position(self, key_id):
        return self.get_position_of(key_id + 97)

    def count_keys(self):
        total_keys = 0
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                item = self.get_item_at(x, y)
                if item >= 97 and item <= 122: # is a key
                    total_keys = total_keys + 1
        return total_keys

    def __init__(self, filename):
        self.grid = []
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
    
    def verify(self):
        return self.test_grid and self.start_point.x == self.expected_start_x and self.start_point.y == self.expected_start_y and self.total_keys == self.expected_total_keys and self.expected_result > 0
    
    def add_routes(self, current_route):
        routes = []
        for next_step in range(0, 4):
            dx = dirs[next_step][0]
            dy = dirs[next_step][1]
            item = self.get_item_at(current_route.point.x + dx, current_route.point.y + dy)
            next_route = current_route.update(next_step, item)
            if next_route != None:
                routes.append(next_route)
        return routes
    
    def walk_to_target(self, point, keychain, target):
        start = chr(self.get_item_at(point.x, point.y))
        routes = [ Route(point, '', keychain) ]
        steps = 0
        while len(routes) > 0:
            new_routes = []
            for route in routes:
                if target in route.keychain:
                    print 'keychain: {}, from {} to {}, steps: {}, route: {}'.format(keychain, start, target, steps, route)
                    return route
                elif len(route.keychain) == len(keychain): # don't collect any other keys before the one we're after
                    new_routes.extend(self.add_routes(route))
            routes = new_routes
            steps = steps + 1
        return None

    def find_targets(self, point, keychain = ''):
        routes = []
        for key_number in range(0, self.total_keys):
            key_value = chr(key_number + 97)
            if key_value not in keychain:
                shortest_route = self.walk_to_target(point, keychain, key_value)
                if shortest_route != None:
                    routes.append(shortest_route)
        return routes

    def get_route_map(self):
        routes = self.find_targets(self.start_point)
        route_map = {}
        count = 0
        while len(routes) > 0:
            count = count + 1
            for route in routes:
                key1 = chr(self.get_item_at(route.points[0].x, route.points[0].y))
                key2 = chr(self.get_item_at(route.point.x, route.point.y))
                if not route_map.has_key(key1):
                    route_map[key1] = {}
                route_map[key1][key2] = len(route.path)
                # print '{} -> {}: {} steps'.format(key1, key2, len(route.path))
            new_routes = []
            print 'Pass {} complete, finding new targets for {} routes'.format(count, len(routes))
            sorted_routes = {}
            for route in routes:
                sorted_keychain = ''.join(sorted(route.keychain[:-1])) + route.keychain[len(route.keychain) - 1]
                if sorted_routes.has_key(sorted_keychain):
                    other = sorted_routes[sorted_keychain]
                    our_len = len(route.path)
                    their_len = len(other.path)
                    # print 'Found similar route to {} ({}) with {} steps, we have {}'.format(route.keychain, other.keychain, their_len, our_len)
                    if their_len <= our_len:
                        route.dead = True
                    else:
                        other.dead = True
                else:
                    sorted_routes[sorted_keychain] = route
            for route in routes:
                if not route.dead:
                    # print 'Finding new targets for route {}'.format(route.keychain)
                    new_routes.extend(self.find_targets(route.point, route.keychain))
            routes = new_routes
        return route_map

    def walk_with_map(self, route_map, start_item, keys_required):
        if keys_required == 0 or not route_map.has_key(start_item):
            return []
        steps = {}
        for next_item in route_map[start_item]:
            if keys_required == 1:
                steps[start_item + next_item] = route_map[start_item][next_item]
                print '{} steps from {} to {}'.format(route_map[start_item][next_item], start_item, next_item)
            else:
                next_steps = self.walk_with_map(route_map, next_item, keys_required - 1)
                if len(next_steps) > 0:
                    for next_step in next_steps:
                        if start_item not in next_step:
                            steps[start_item + next_step] = route_map[start_item][next_item] + next_steps[next_step]
                            print '{} steps on route {}'.format(steps[start_item + next_step], start_item + next_step)
        return steps

    def walk(self):
        steps = self.walk_with_map(self.get_route_map(), '@', self.total_keys)
        min_steps = ''
        for route in steps:
            if min_steps == '' or steps[min_steps] > steps[route]:
                print 'Found minimum for {}: {} steps'.format(route, steps[route])
                min_steps = route
        return [ min_steps, steps[min_steps] ]

def run_tests():
    for maze_id in range(1, 2):
        filename = 'day18-test-grid-{}.txt'.format(maze_id + 1)
        test_maze = Maze(filename)
        print 'Test maze loaded correctly: {}'.format(test_maze.verify())
        if maze_id == 3:
            print 'Skipping walk (too slow).'
        else:
            route = test_maze.walk()
            if route == None:
                print 'Did not find a route.'
            else:
                print 'Found route: {}'.format(str(route))
                print 'Expected route found: {}'.format(test_maze.expected_result == route[1])

run_tests()

# filename = 'day18-input.txt'
# maze = Maze(filename)
# print 'Maze {}: start ({}, {}), {} keys'.format(filename, maze.start_point.x, maze.start_point.y, maze.total_keys)

# route = maze.walk()
# print 'Found route: {}'.format(str(route))