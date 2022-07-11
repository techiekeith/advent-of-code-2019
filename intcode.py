#!/usr/bin/python
import fileinput
import sys

initial_args = sys.argv[1:]

class IntcodeMachine:
	init_state = []
	state = []
	inputs = []
	outputs = []
	program_counter = 0
	relative_base = 0
	waiting = False
	stopped = False
	error = False

	def add(self, args):
		self.state[args[2]] = args[0] + args[1]
		self.program_counter = self.program_counter + 4

	def multiply(self, args):
		self.state[args[2]] = args[0] * args[1]
		self.program_counter = self.program_counter + 4

	def get_input(self, args):
		if len(self.inputs) == 0:
			self.waiting = True
		else:
			value = self.inputs.pop(0)
			self.state[args[0]] = int(value)
			self.program_counter = self.program_counter + 2

	def add_output(self, args):
		self.outputs.append(args[0])
		self.program_counter = self.program_counter + 2

	def jump_if_true(self, args):
		if args[0] == 0:
			self.program_counter = self.program_counter + 3
		else:
			self.program_counter = args[1]

	def jump_if_false(self, args):
		if args[0] == 0:
			self.program_counter = args[1]
		else:
			self.program_counter = self.program_counter + 3

	def less_than(self, args):
		if args[0] < args[1]:
			self.state[args[2]] = 1
		else:
			self.state[args[2]] = 0
		self.program_counter = self.program_counter + 4

	def equals(self, args):
		if args[0] == args[1]:
			self.state[args[2]] = 1
		else:
			self.state[args[2]] = 0
		self.program_counter = self.program_counter + 4

	def relative_base_offset(self, args):
		self.relative_base = self.relative_base + args[0]
		self.program_counter = self.program_counter + 2

	operations = [ add, multiply, get_input, add_output, jump_if_true, jump_if_false, less_than, equals, relative_base_offset ]
	num_operands = [ 3, 3, 1, 1, 2, 2, 3, 3, 1 ]
	write_arguments = [ 3, 3, 1, -1, -1, -1, 3, 3, -1 ]

	def add_input(self, input):
		self.inputs.append(input)
		if self.waiting:
			self.waiting = False
			self.run()

	def read_output(self):
		if (len(self.outputs) == 0):
			return None
		return self.outputs.pop(0)

	def read_outputs(self):
		values = []
		values.extend(self.outputs)
		del self.outputs[:]
		return values

	def set_mem(self, position, value):
		while position >= len(self.state):
			self.state.append(0)
		self.state[position] = value

	def load_code(self, code):
		self.init_state = []
		for opcode in code.split(','):
			self.init_state.append(int(opcode))
		self.state = []
		self.state.extend(self.init_state)

	def load_from_file(self, filename):
		for line in fileinput.input(files=(filename)):
			self.load_code(line)

	def reset(self):
		self.state = []
		self.state.extend(self.init_state)
		self.inputs = []
		self.outputs = []
		self.program_counter = 0
		self.relative_base = 0
		self.waiting = False
		self.stopped = False
		self.error = False

	def is_waiting(self):
		return self.waiting

	def is_stopped(self):
		return self.stopped

	def is_error(self):
		return self.error

	def print_state(self):
		flags = ('E' if self.error else ' ') + ('S' if self.stopped else ' ') + ('W' if self.waiting else ' ')
		print '[{}] PC:{} -> {}'.format(flags, self.program_counter, str(self.outputs))

	def run(self):
		while (self.program_counter < len(self.state) and self.state[self.program_counter] != 99 and not self.waiting and not self.error):
			instruction = self.state[self.program_counter]
			modes = instruction // 100
			opcode = instruction % 100
			write_argument = -1
			if (opcode < 1 or opcode > len(self.operations) + 1):
#				print "Error: unknown opcode " + str(opcode)
				self.error = True
			operation = self.operations[opcode - 1]
			num_arguments = self.num_operands[opcode - 1]
			write_argument = self.write_arguments[opcode - 1]
			operands = []
			for i in range(1, num_arguments + 1):
				argument = self.state[self.program_counter + i]
				mode = modes % 10
				# print "i=" + str(i) + " write_argument=" + str(write_argument) + " argument=" + str(argument) + " mode=" + str(mode)
				if mode == 1:
					if i == write_argument:
#						print "Error: write argument cannot be in immediate mode"
						self.error = True
					else:
						operands.append(argument)
				else:
					if mode == 2:
						argument = argument + self.relative_base
					while argument >= len(self.state):
						self.state.append(0)
					if argument < 0:
#						print "Error: read position " + str(argument) + " out of bounds"
						self.error = True
					elif i == write_argument:
						operands.append(argument)
					else:
						operands.append(self.state[argument])
				modes = modes // 10
#			print 'PC=' + str(self.program_counter) + ' inputs=' + str(self.inputs) + ' outputs=' + str(self.outputs) + ' operands=' + str(operands) + ' operation=' + str(operation)
			operation(self, operands)
		if (self.state[self.program_counter] == 99):
			self.stopped = True
		elif (not self.waiting):
			self.error = True
