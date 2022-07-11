import fileinput
import sys

#
# A class for representing a point in a two-dimensional space.
#
class Point3D:
	x = 0
	y = 0
	z = 0
	moves = 0

	def __init__(self, x = 0, y = 0, z = 0, moves = 0):
		self.x = x
		self.y = y
		self.z = z
		self.moves = moves

	def __str__(self):
		return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

	def __repr__(self):
		return 'Point(' + str(self) + ')'

	def __hash__(self):
		return hash(self.__repr__())

	def __cmp__(self, other):
		retval = cmp(abs(self.x) + abs(self.y) + abs(self.z), abs(other.x) + abs(other.y) + abs(other.z))
		if retval == 0:
			retval = cmp(self.z, other.z)
		if retval == 0:
			retval = cmp(self.y, other.y)
		if retval == 0:
			retval = cmp(self.x, other.x)
		return retval

	def add(self, x, y, z = 0):
		return Point3D(self.x + x, self.y + y, self.z + z, self.moves + abs(x) + abs(y) + abs(z))

	def equals(self, other):
		return cmp(self, other) == 0
