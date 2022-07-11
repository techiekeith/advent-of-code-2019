import fileinput
import sys

state = []

for line in fileinput.input(files=('day2-input.txt')):
	for opcode in line.split(','):
		state.append(int(opcode))

print state

state[1] = int(sys.argv[1])
state[2] = int(sys.argv[2])

pc = 0
while (pc < len(state) and state[pc] != 99):
	opcode = state[pc]
	source1 = state[pc + 1]
	operand1 = state[source1]
	source2 = state[pc + 2]
	operand2 = state[source2]
	target = state[pc + 3]
	if (opcode == 1):
		print '[' + str(pc) + ']: *' + str(target) + ' = (*' + str(source1) + ') ' + str(operand1) + ' + ' + str(operand2) + ' (*' + str(source2) + ')'
		state[target] = operand1 + operand2
		pc = pc + 4
	elif (opcode == 2):
		print '[' + str(pc) + ']: *' + str(target) + ' = (*' + str(source1) + ') ' + str(operand1) + ' * ' + str(operand2) + ' (*' + str(source2) + ')'
		state[target] = operand1 * operand2
		pc = pc + 4
	else:
		print "Error: unknown opcode " + str(opcode)

if (pc < len(state) and state[pc] == 99):
	print '[' + str(pc) + ']: End'

print state
