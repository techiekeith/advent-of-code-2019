import curses
from intcode import IntcodeMachine
from point import Point

dirs = 'URDL'
robot = '^>v<'
hull = { Point(): 1 }

def get_color_at(point):
    return hull[point] if hull.has_key(point) else 0

def set_color_at(point, color):
    hull[point] = color

def main(stdscr):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    dir = 0
    point = Point()
    stdscr.clear()
    intcode = IntcodeMachine()
    intcode.load_from_file('day11-input.txt')
    while not intcode.is_stopped():
        intcode.add_input(get_color_at(point))
        intcode.run()
        values = intcode.read_outputs()
        if (len(values)) != 0:
            set_color_at(point, int(values[0]))
            dir = (dir + (-1 if int(values[1]) == 0 else 1)) % 4
            point = point.move(dirs[dir])
            if min_x > point.x:
                min_x = point.x
            if max_x < point.x:
                max_x = point.x
            if min_y > point.y:
                min_y = point.y
            if max_y < point.y:
                max_y = point.y
            for line in range(0, max_y - min_y + 1):
                for column in range(0, max_x - min_x + 1):
                    display_point = Point(column + min_x, line + min_y)
                    if display_point.x == point.x and display_point.y == point.y:
                        pixel = robot[dir]
                    elif get_color_at(display_point) == 1:
                        pixel = '#'
                    else:
                        pixel = '.'
                    if line < curses.LINES - 1 and column < curses.COLS:
                        stdscr.addstr(curses.LINES - line - 1, column, pixel)
        stdscr.addstr(0, 0, '[ Panels painted: {} ]'.format(len(hull)))
        stdscr.addstr(0, 30, '[ {} {} {} ]'.format(values, point, dir))
        stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)
