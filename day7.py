#!/usr/bin/python
import fileinput
import sys

initial_args = sys.argv[1:]

class IntcodeMachine:
	program_filename = 'day7-input.txt'
	state = []
	inputs = []
	outputs = []
	pc = 0
	waiting = False
	stopped = False
	error = False

	def add(self, args):
		self.state[args[2]] = args[0] + args[1]
		self.pc = self.pc + 4

	def multiply(self, args):
		self.state[args[2]] = args[0] * args[1]
		self.pc = self.pc + 4

	def input(self, args):
		if len(self.inputs) == 0:
			self.waiting = True
		else:
			value = self.inputs.pop(0)
			self.state[args[0]] = int(value)
			self.pc = self.pc + 2

	def output(self, args):
		self.outputs.append(str(args[0]))
		self.pc = self.pc + 2

	def jump_if_true(self, args):
		if args[0] == 0:
			self.pc = self.pc + 3
		else:
			self.pc = args[1]

	def jump_if_false(self, args):
		if args[0] == 0:
			self.pc = args[1]
		else:
			self.pc = self.pc + 3

	def less_than(self, args):
		if args[0] < args[1]:
			self.state[args[2]] = 1
		else:
			self.state[args[2]] = 0
		self.pc = self.pc + 4

	def equals(self, args):
		if args[0] == args[1]:
			self.state[args[2]] = 1
		else:
			self.state[args[2]] = 0
		self.pc = self.pc + 4

	operations = [ add, multiply, input, output, jump_if_true, jump_if_false, less_than, equals ]
	num_operands = [ 3, 3, 1, 1, 2, 2, 3, 3 ]
	write_arguments = [ 3, 3, 1, -1, -1, -1, 3, 3 ]

	def add_input(self, input):
		self.inputs.append(input)
		if self.waiting:
			self.waiting = False
			self.run()

	def read_output(self):
		if (len(self.outputs) == 0):
			print "Error! No output to read"
			return None
		return self.outputs.pop(0)

	def load_code(self, code):
		for opcode in code.split(','):
			self.state.append(int(opcode))

	def load_from_file(self):
		for line in fileinput.input(files=(self.program_filename)):
			self.load_code(line)

	def reset(self):
		self.state = []
		self.inputs = []
		self.outputs = []
		self.pc = 0
		self.waiting = False
		self.stopped = False
		self.error = False

	def is_waiting(self):
		return self.waiting

	def is_stopped(self):
		return self.stopped

	def is_error(self):
		return self.error

	def run(self):
		while (self.pc < len(self.state) and self.state[self.pc] != 99 and not self.waiting):
			instruction = self.state[self.pc]
			modes = instruction // 100
			opcode = instruction % 100
			write_argument = -1
			if (opcode < 1 or opcode > len(self.operations) + 1):
				print "Error: unknown opcode " + str(opcode)
				exit(1)
			operation = self.operations[opcode - 1]
			num_arguments = self.num_operands[opcode - 1]
			write_argument = self.write_arguments[opcode - 1]
			operands = []
			for i in range(1, num_arguments + 1):
				argument = self.state[self.pc + i]
				mode = modes % 10
				# print "i=" + str(i) + " write_argument=" + str(write_argument) + " argument=" + str(argument) + " mode=" + str(mode)
				if i == write_argument and mode == 1:
					print "Error: write argument cannot be in immediate mode"
					exit(1)
				elif mode == 0:
					if argument < 0 or argument >= len(self.state):
						print "Error: read position " + str(argument) + " out of bounds"
						exit(1)
					elif i == write_argument:
						operands.append(argument)
					else:
						operands.append(self.state[argument])
				else:
					operands.append(argument)
				modes = modes // 10
#			print 'PC=' + str(self.pc) + ' inputs=' + str(self.inputs) + ' outputs=' + str(self.outputs) + ' operands=' + str(operands) + ' operation=' + str(operation)
			operation(self, operands)
		if (self.state[self.pc] == 99):
			self.stopped = True
		elif (not self.waiting):
			self.error = True

def test_code(machines, phases):
	for i in range(0, len(phases)):
		machines[i].reset()
		machines[i].load_from_file()
		machines[i].add_input(phases[i])
	value = 0
	running = True
	while running:
		running = False
		for i in range(0, len(phases)):
			if not machines[i].is_stopped():
				machines[i].add_input(value)
				machines[i].run()
				value = machines[i].read_output()
#				print str(i) + ': [Output:' + str(value) + ', Waiting:' + str(machines[i].is_waiting()) + ', Stopped:' + str(machines[i].is_stopped()) + ', Error:' + str(machines[i].is_error()) + ']'
				running = running or not machines[i].is_stopped()
	print str(phases) + ': ' + str(value)

machines = [ IntcodeMachine(), IntcodeMachine(), IntcodeMachine(), IntcodeMachine(), IntcodeMachine() ]

start_phase = 5
end_phase = 9

for i in range(start_phase, end_phase + 1):
	for j in range(start_phase, end_phase + 1):
		if i != j:
			for k in range(start_phase, end_phase + 1):
				if i != k and j != k:
					for l in range(start_phase, end_phase + 1):
						if i != l and j != l and k != l:
							for m in range(start_phase, end_phase + 1):
								if i != m and j != m and k != m and l != m:
									test_code(machines, [ i, j, k, l, m ])

