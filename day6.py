import fileinput

orbits = {}

for line in fileinput.input():
	parts = line.strip().split(')')
	orbits[parts[1]] = parts[0]
	print parts[0] + ' ) ' + parts[1]

checksum = 0

you_orbits = []
san_orbits = []

for body in orbits:
	start_body = body
	sequence = [ body ]
	while orbits[body] in orbits:
		body = orbits[body]
		sequence.append(body)
	num_orbits = len(sequence)
	sequence.append(orbits[body])
	print str(sequence) + ': ' + str(num_orbits) + ' orbits'
	if start_body == 'YOU':
		you_orbits = sequence
	if start_body == 'SAN':
		san_orbits = sequence
	checksum = checksum + num_orbits

print 'Checksum: ' + str(checksum)

print 'YOU: ' + str(you_orbits)
print 'SAN: ' + str(san_orbits)

a = you_orbits.pop()
b = san_orbits.pop()
last = ''
while a == b:
	print a + '=' + b
	last = a
	a = you_orbits.pop()
	b = san_orbits.pop()

print a + '!=' + b

path = []
path.extend(you_orbits)
path.append(a)
path.append(last)
path.append(b)
san_orbits.reverse()
path.extend(san_orbits)

num_transfers = len(path) - 3 # Don't count YOU or SAN
print 'YOU->SAN: ' + str(path) + ': ' + str(num_transfers) + ' orbital transfers'
