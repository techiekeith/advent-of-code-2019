import curses
import time
from intcode import IntcodeMachine
from point import Point

class MapperDroid:
    point_dirs = 'URDL'
    input_dirs = [ 1, 4, 2, 3 ]
    ship = { Point(): 1 }
    droid = Point()
    oxygen_tank = None
    window = None
    machine = None

    def __init__(self, window):
        self.window = window
        self.machine = IntcodeMachine()
        self.machine.load_from_file('day15-input.txt')
        self.machine.run()

    def render(self):
        if self.window == None:
            return
        # min_x = self.droid.x - curses.COLS // 2
        # min_y = self.droid.y - curses.LINES // 2
        min_x = -curses.COLS // 2
        min_y = -curses.LINES // 2
        max_x = min_x + curses.COLS - 1
        max_y = min_y + curses.LINES - 1

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                point = Point(x, y)
                if point.x == self.droid.x and point.y == self.droid.y:
                    pixel = 'D'
                elif self.ship.has_key(point):
                    if self.ship[point] == 0:
                        pixel = '#'
                    elif self.ship[point] == 2:
                        pixel = 'O'
                    else:
                        pixel = '.'
                else:
                    pixel = '~'
                self.window.addstr(y - min_y, x - min_x, pixel)
        self.window.addstr(0, 0, 'Pos: ({}, {})'.format(self.droid.x, self.droid.y))
        self.window.refresh()

    def follow_route(self, route):
        for droid_dir in route:
            # print 'Following: {}'.format(droid_dir)
            self.droid = self.droid.move(self.point_dirs[int(droid_dir)])
            self.machine.add_input(self.input_dirs[int(droid_dir)])
            tile = self.machine.read_output()
            if int(tile) == 0:
                print 'Error! ran into wall following existing route'
                exit(1)

    def retrace_route(self, route):
        for droid_dir in reversed(route):
            # print 'Retracing: {}'.format(droid_dir)
            reverse_dir = (int(droid_dir) + 2) % 4
            self.droid = self.droid.move(self.point_dirs[reverse_dir])
            self.machine.add_input(self.input_dirs[reverse_dir])
            tile = self.machine.read_output()
            if int(tile) == 0:
                print 'Error! ran into wall retracing steps'
                exit(1)

    def get_more_routes(self, current_route = ''):
        self.follow_route(current_route)
        routes = {}
        for droid_dir in range(0, 4):
            next_point = self.droid.move(self.point_dirs[droid_dir])
            if not self.ship.has_key(next_point):
                self.machine.add_input(self.input_dirs[droid_dir])
                tile = int(self.machine.read_output())
                # print 'droid dir {} / input dir {}: {}'.format(droid_dir, self.input_dirs[droid_dir], tile)
                self.ship[next_point] = tile
                if tile != 0:
                    next_route = current_route + str(droid_dir)
                    # print 'Next route: {}'.format(next_route)
                    routes[next_route] = tile
                    self.machine.add_input(self.input_dirs[(droid_dir + 2) % 4])
                    tile = self.machine.read_output()
                    if int(tile) == 0:
                        print 'Error! ran into wall retracing steps'
                        exit(1)
                self.render()
        self.retrace_route(current_route)
        return routes
    
    def walk(self):
        oxygen_tank = ''
        routes = self.get_more_routes()
        while len(routes) > 0:
            new_routes = {}
            for route in routes:
                # print 'Route {}: {}'.format(route, routes[route])
                if routes[route] == 2:
                    # print 'Found tank at {}'.format(route)
                    oxygen_tank = route
                add_routes = self.get_more_routes(route)
                for add_route in add_routes:
                    new_routes[add_route] = add_routes[add_route]
            routes = new_routes
        return oxygen_tank

    def get_map_bounds(self):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for point in self.ship:
            if min_x > point.x:
                min_x = point.x
            if min_y > point.y:
                min_y = point.y
            if max_x < point.x:
                max_x = point.x
            if max_y < point.y:
                max_y = point.y
        return [ min_x, min_y, max_x, max_y ]

    def spread_oxygen(self):
        for point in self.ship:
            if self.ship[point] == 2:
                for oxygen_dir in range(0, 4):
                    next_point = point.move(self.point_dirs[oxygen_dir])
                    if self.ship.has_key(next_point) and self.ship[next_point] == 1:
                        self.ship[next_point] = 3
        complete = True
        for point in self.ship:
            if self.ship[point] == 1:
                complete = False
            elif self.ship[point] == 3:
                self.ship[point] = 2
        self.render()
        return complete

def main(window):
    if window != None:
        window.clear()
    mapper_droid = MapperDroid(window)
    found_route = mapper_droid.walk()
    iterations = 0
    complete = False
    while not complete:
        complete = mapper_droid.spread_oxygen()
        iterations = iterations + 1
    if window != None:
        window.addstr(0, 0, 'Fastest route: {} steps; oxygen replenished in {} minutes'.format(len(found_route), iterations))
        window.getkey()

curses.wrapper(main)
# main(None)