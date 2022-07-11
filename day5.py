import fileinput
import sys

def add(args):
	# print args
	state[args[2]] = args[0] + args[1]
	return pc + 4

def multiply(args):
	# print args
	state[args[2]] = args[0] * args[1]
	return pc + 4

def input(args):
	line = raw_input('Enter value: ')
	state[args[0]] = int(line.rstrip())
	return pc + 2

def output(args):
	print str(args[0])
	return pc + 2

def jump_if_true(args):
	if args[0] == 0:
		return pc + 3
	else:
		return args[1]

def jump_if_false(args):
	if args[0] == 0:
		return args[1]
	else:
		return pc + 3

def less_than(args):
	if args[0] < args[1]:
		state[args[2]] = 1
	else:
		state[args[2]] = 0
	return pc + 4

def equals(args):
	if args[0] == args[1]:
		state[args[2]] = 1
	else:
		state[args[2]] = 0
	return pc + 4

pc = 0
state = []

operations = [ add, multiply, input, output, jump_if_true, jump_if_false, less_than, equals ]
num_operands = [ 3, 3, 1, 1, 2, 2, 3, 3 ]
write_arguments = [ 3, 3, 1, -1, -1, -1, 3, 3 ]

if len(sys.argv) > 1:
	line = sys.argv[1]
	for opcode in line.split(','):
		state.append(int(opcode))
else:
	for line in fileinput.input(files=('day5-input.txt')):
		for opcode in line.split(','):
			state.append(int(opcode))

while (pc < len(state) and state[pc] != 99):
	instruction = state[pc]
	modes = instruction // 100
	opcode = instruction % 100
	write_argument = -1
	if (opcode < 1 or opcode > len(operations) + 1):
		print "Error: unknown opcode " + str(opcode)
		exit(1)
	operation = operations[opcode - 1]
	num_arguments = num_operands[opcode - 1]
	write_argument = write_arguments[opcode - 1]
	operands = []
	for i in range(1, num_arguments + 1):
		argument = state[pc + i]
		mode = modes % 10
		# print "i=" + str(i) + " write_argument=" + str(write_argument) + " argument=" + str(argument) + " mode=" + str(mode)
		if i == write_argument and mode == 1:
			print "Error: write argument cannot be in immediate mode"
			exit(1)
		elif mode == 0:
			if argument < 0 or argument >= len(state):
				print "Error: read position " + str(argument) + " out of bounds"
				exit(1)
			elif i == write_argument:
				operands.append(argument)
			else:
				operands.append(state[argument])
		else:
			operands.append(argument)
		modes = modes // 10
	pc = operation(operands)

if (pc < len(state)):
	print '[' + str(pc) + ']: End'
else:
	print '[' + str(pc) + ']: Unexpected EOF'

print state

