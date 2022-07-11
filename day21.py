import fileinput
from intcode import IntcodeMachine

class SpringDroid:
    def __init__(self):
        self.machine = IntcodeMachine()
        self.machine.load_from_file('day21-input.txt')

    def render_output(self):
        output_codes = self.machine.read_outputs()
        output = ''
        for i in output_codes:
            if i == 9 or i == 10 or (i >= 32 and i < 127):
                output += chr(i)
            else:
                output += ' [{}] '.format(i)
        print output

    def program(self, lines):
        self.machine.reset()
        self.machine.run()
        self.render_output()
        for line in lines:
            for code in line:
                self.machine.add_input(ord(code))
            self.machine.add_input(10)

    def render(self):
        self.render_output()
        self.machine.print_state()

droid = SpringDroid()

droid.program([ 'NOT A J', 'NOT B T', 'AND D T', 'AND A T', 'OR T J', 'NOT C T', 'AND D T', 'AND A T', 'OR T J', 'WALK' ]) 
droid.render()

droid.program([ 'NOT A J', 'NOT B T', 'AND D T', 'AND H T', 'OR T J', 'NOT C T', 'AND D T', 'AND H T', 'OR T J', 'RUN' ])
droid.render()
