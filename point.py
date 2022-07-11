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
