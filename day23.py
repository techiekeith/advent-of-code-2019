import curses
import sys
from intcode import IntcodeMachine

class Network:
    total_machines = 50
    nat = 255

    def __init__(self):
        self.clock = 0
        self.machines = {}
        self.packet_queue = {}
        self.nat_buffer = [ -1, -1 ]
        self.last_nat_buffer = [ -1, -1 ]
        self.unmatched_packets = []
        self.window = None
        for address in range(0, Network.total_machines):
            machine = IntcodeMachine()
            machine.load_from_file('day23-input.txt')
            machine.run()
            machine.add_input(address)
            self.machines[address] = machine
            self.packet_queue[address] = []
    
    def poll(self):
        for address in range(0, Network.total_machines):
            machine = self.machines[address]
            outputs = machine.read_outputs()
            packet_size = 3
            packets = [outputs[i * packet_size:(i + 1) * packet_size] for i in range(0, len(outputs) // packet_size)]
            for [ destination, x, y ] in packets:
                if self.machines.has_key(destination):
                    self.packet_queue[destination].append(x)
                    self.packet_queue[destination].append(y)
                    if self.window == None:
                        print "{} -> {}: x={}, y={}".format(address, destination, x, y)
                elif destination == Network.nat:
                    self.nat_buffer = [x, y]
                    if self.window == None:
                        print "{} -> NAT: x={}, y={}".format(address, x, y)
                else:
                    self.unmatched_packets.extend([destination, x, y])
                    if self.window == None:
                        print "Unknown destination {} (src={}, x={}, y={})".format(destination, address, x, y)

    def dequeue_packets(self):
        if self.window != None:
            self.window.addstr("Clock: {}".format(self.clock))
        idle = True
        for address in range(0, Network.total_machines):
            machine = self.machines[address]
            if len(self.packet_queue[address]) == 0:
                machine.add_input(-1)
                output_string = '-------'
            else:
                idle = False
                x = self.packet_queue[address].pop(0)
                y = self.packet_queue[address].pop(0)
                machine.add_input(x)
                machine.add_input(y)
                output_string = '{x:-3d},{y:-3d}'.format(x=x, y=y)
            if self.window != None:
                line = (address // 8) * 5 + 3
                column = (address % 8) * 10
                self.window.addstr(line, column, "[ #{} ]".format(address))
                self.window.addstr(line + 2, column, "[ #{} ]".format(address))
        self.idle = idle
        self.clock += 1

    def dequeue_nat_packet_if_idle(self):
        if self.idle and self.nat_buffer[0] >= 0:
            self.packet_queue[0].extend(self.nat_buffer)
            if self.nat_buffer[1] == self.last_nat_buffer[1] and self.window == None:
                print "*** Repeated ***: {}".format(self.nat_buffer)
                exit(1)
            self.last_nat_buffer = []
            self.last_nat_buffer.extend(self.nat_buffer)

def main(window = None):
    if window != None:
        window.clear()
    network = Network()
    while True:
        network.poll()
        network.dequeue_packets()
        network.dequeue_nat_packet_if_idle()
        if window != None:
            window.getkey()
    if window != None:
        window.refresh()
        window.getkey()

if len(sys.argv) > 1 and sys.argv[1] == '-w':
    curses.wrapper(main)
else:
    main()
