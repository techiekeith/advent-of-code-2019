import fileinput
import sys

#
# A class for representing a point in a two-dimensional space.
#
class Point:
	x = 0
	y = 0
	moves = 0

	def __init__(self, x = 0, y = 0, moves = 0):
		self.x = x
		self.y = y
		self.moves = moves

	def __repr__(self):
		return 'Point(' + str(self.x) + ', ' + str(self.y) + ')'

	def __str__(self):
		return '(' + str(self.x) + ',' + str(self.y) + ')'

	def __hash__(self):
		return hash(self.__repr__())

	def __cmp__(self, other):
		retval = cmp(abs(self.x) + abs(self.y), abs(other.x) + abs(other.y))
		if retval == 0:
			retval = cmp(self.y, other.y)
		if retval == 0:
			retval = cmp(self.x, other.x)
		return retval

	def add(self, x, y):
		return Point(self.x + x, self.y + y, self.moves + abs(x) + abs(y))

	def equals(self, other):
		return cmp(self, other) == 0

	def manhattan_distance_from(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y)

	def move(self, dir):
		if dir == 'R':
			dx = 1
		elif dir == 'L':
			dx = -1
		else:
			dx = 0
		if dir == 'U':
			dy = 1
		elif dir == 'D':
			dy = -1
		else:
			dy = 0
		return self.add(dx, dy)

#
# Parses a line of move instructions.
#
def parse_line(input_line):
	line = []
	point = Point()
	for instruction in input_line.split(','):
		dir = instruction[0]
		amount = int(instruction[1:])
		for i in range(0, amount):
			point = point.move(dir)
			line.append(point)
	return line

#
# For storing our lines
#
input_lines = []

#
# Read lines from file
#
for input_line in fileinput.input(files=('day3-input.txt')):
	input_lines.append(parse_line(input_line))

#
# Get points common to both lines
#
first_row = input_lines[0]
second_row = input_lines[1]

matching_points = set(first_row) & set(second_row)

#
# Get total steps for each matching point
#
ordered_points = []

for matching_point in matching_points:
	first_point = first_row[first_row.index(matching_point)]
	second_point = second_row[second_row.index(matching_point)]
	point = Point(first_point.x, first_point.y, first_point.moves + second_point.moves)
	print str(point) + ' total steps: ' + str(point.moves)
	print str(first_point.moves) + ' + ' + str(second_point.moves)
	ordered_points.append(point)

ordered_by_distance = ordered_points
ordered_by_distance.sort()

print 'Closest: ' + str(ordered_by_distance[0])
print 'Manhattan distance: ' + str(ordered_by_distance[0].manhattan_distance_from(Point()))
print 'Total steps: ' + str(ordered_by_distance[0].moves)

ordered_by_length = ordered_points
ordered_by_length.sort(key = lambda x: x.moves)

print 'Shortest: ' + str(ordered_by_length[0])
print 'Manhattan distance: ' + str(ordered_by_length[0].manhattan_distance_from(Point()))
print 'Total steps: ' + str(ordered_by_length[0].moves)


