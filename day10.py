import fileinput
import math
import sys

def get_intervals(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return [ 0, 0, 0 ]
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        intervals = abs(dy)
    elif dy == 0:
        intervals = abs(dx)
    else:
        max_root = int(min(abs(dx), abs(dy)))
        intervals = 1
        root = 1
        while root < max_root:
            root = root + 1
            if dx % root == 0 and dy % root == 0:
                intervals = root
    step_x = dx / intervals
    step_y = dy / intervals
    # print "(" + str(x1) + "," + str(y1) + ") -> (" + str(x2) + "," + str(y2) + ") = (" + str(dx) + "," + str(dy) + "): " + str(intervals) + " x (" + str(step_x) + "," + str(step_y) + ")"
    return [ intervals, step_x, step_y ]

def is_visible(asteroid_map, x1, y1, x2, y2):
    [ intervals, step_x, step_y ] = get_intervals(x1, y1, x2, y2)
    x = x1
    y = y1
    visible = True
    for point in range(1, intervals):
        x = x + step_x
        y = y + step_y
        if asteroid_map[y][x] == '#':
            # print "(" + str(x) + "," + str(y) + ") contains an asteroid"
            visible = False
            break
        # else:
            # print "(" + str(x) + "," + str(y) + ") is clear"
    return visible

def count_visible_asteroids(asteroid_map, station_x, station_y):
    rows = len(asteroid_map)
    columns = len(asteroid_map[0])
    visible_asteroids = 0
    for y in range(0, rows):
        for x in range(0, columns):
            if asteroid_map[y][x] == '#' and (x != station_x or y != station_y):
                if is_visible(asteroid_map, station_x, station_y, x, y):
                    visible_asteroids = visible_asteroids + 1
    return visible_asteroids

def load_map_from_file():
    asteroid_map = []
    for line in fileinput.input(files=('day10-input.txt')):
        asteroid_map.append(line.strip())
    return asteroid_map

# asteroid_map = []
# asteroid_map.append('......#.#.')
# asteroid_map.append('#..#.#....')
# asteroid_map.append('..#######.')
# asteroid_map.append('.#.#.###..')
# asteroid_map.append('.#..#.....')
# asteroid_map.append('..#....#.#')
# asteroid_map.append('#..#....#.')
# asteroid_map.append('.##.#..###')
# asteroid_map.append('##...#..#.')
# asteroid_map.append('.#....####')

asteroid_map = load_map_from_file()

rows = len(asteroid_map)
columns = len(asteroid_map[0])

max_visible_asteroids = 0
best_x = -1
best_y = -1

for y in range(0, rows):
    for x in range(0, columns):
        if asteroid_map[y][x] == '#':
            visible_asteroids = count_visible_asteroids(asteroid_map, x, y)
            # print "(" + str(x) + "," + str(y) + "): " + str(visible_asteroids) + " visible asteroids"
            if max_visible_asteroids < visible_asteroids:
                # print "Better location: (" + str(x) + "," + str(y) + "): " + str(visible_asteroids) + " visible asteroids"
                max_visible_asteroids = visible_asteroids
                best_x = x
                best_y = y

print "Best location: (" + str(best_x) + "," + str(best_y) + "): " + str(max_visible_asteroids) + " visible asteroids"

asteroids = []

for y in range(0, rows):
    for x in range(0, columns):
        if asteroid_map[y][x] == '#' and (x != best_x or y != best_y):
            dx = x - best_x
            dy = y - best_y
            distance = math.sqrt(dx * dx + dy * dy)
            angle = math.acos(-dy / distance) * 180 / math.pi
            if dx < 0:
                angle = 360 - angle
            angle = math.floor(angle * 1000) / 1000
            # print "Asteroid @ (" + str(x) + "," + str(y) + "): " + str(distance) + " " + str(angle)
            asteroids.append([ x, y, angle, distance ])

def comparator_function(a, b):
    x = cmp(a[2], b[2])
    if x == 0:
        return cmp(a[3], b[3])
    else:
        return x

asteroids.sort(cmp=comparator_function)

count = 0
while count < len(asteroids):
    last_angle = -1
    for i in range(0, len(asteroids)):
        [ x, y, angle, distance ] = asteroids[i]
        if angle >= 0 and angle != last_angle:
            count = count + 1
            print str(count) + ": Vaporized asteroid #" + str(i) + " @ (" + str(x) + "," + str(y) + "): " + str(distance) + " " + str(angle)
            asteroids[i][2] = -1
            last_angle = angle

# print asteroids