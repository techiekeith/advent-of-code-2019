#!/usr/bin/python
import fileinput
import sys

initial_args = sys.argv[1:]

class IntcodeMachine:
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
		self.outputs.append(str(args[0]))
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
		if len(self.outputs) == 0:
			return None
		return self.outputs.pop(0)

	def load_code(self, code):
		for opcode in code.split(','):
			self.state.append(int(opcode))

	def load_from_file(self, filename):
		for line in fileinput.input(files=(filename)):
			self.load_code(line)

	def reset(self):
		self.state = []
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

	def run(self):
		while (self.program_counter < len(self.state) and self.state[self.program_counter] != 99 and not self.waiting and not self.error):
			instruction = self.state[self.program_counter]
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
				argument = self.state[self.program_counter + i]
				mode = modes % 10
				# print "i=" + str(i) + " write_argument=" + str(write_argument) + " argument=" + str(argument) + " mode=" + str(mode)
				if mode == 1:
					if i == write_argument:
						print "Error: write argument cannot be in immediate mode"
						self.error = True
					else:
						operands.append(argument)
				else:
					if mode == 2:
						argument = argument + self.relative_base
					while argument >= len(self.state):
						self.state.append(0)
					if argument < 0:
						print "Error: read position " + str(argument) + " out of bounds"
						exit(1)
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

def print_output(machine):
	values = []
	value = machine.read_output()
	while value != None:
		values.append(value)
		value = machine.read_output()
	print 'Error: ' + str(machine.is_error()) + ' Waiting: ' + str(machine.is_waiting()) + ' Output: ' + str(values)

machine = IntcodeMachine()
machine.load_code('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')
machine.run()
print_output(machine)

machine.reset()
machine.load_code('1102,34915192,34915192,7,4,7,99,0')
machine.run()
print_output(machine)

machine.reset()
machine.load_code('104,1125899906842624,99')
machine.run()
print_output(machine)

machine.reset()
machine.load_from_file('day9-input.txt')
machine.add_input('1')
machine.run()
print_output(machine)

machine.reset()
machine.load_from_file('day9-input.txt')
machine.add_input('2')
machine.run()
print_output(machine)
