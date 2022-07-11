import fileinput

sum = 0

def fuel_needed(mass):
	fuel = (mass / 3) - 2
	if (fuel <= 0):
		fuel = 0
	else:
		fuel = fuel + fuel_needed(fuel)
	print '[' + str(mass) + ' -> ' + str(fuel) + ']'
	return fuel

for line in fileinput.input(files=('day1-input.txt')):
	a = int(line)
	b = fuel_needed(a)
	print str(a) + ' => ' + str(b)
	sum += b

print sum
