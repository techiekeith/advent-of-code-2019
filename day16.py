import fileinput

base_pattern = [ 0, 1, 0, -1 ]

def read_data_from_file(filename):
    for line in fileinput.input(files=(filename)):
        data = line.strip()
    return data

def get_digit_value(signal, size, repeat):
    sum = 0
    for position in range(0, size):
        multiplier = base_pattern[((position + 1) // repeat) % len(base_pattern)]
        if multiplier != 0:
            sum = sum + int(signal[position]) * multiplier
    return str(sum)[-1:]

def apply_pattern_fast(signal):
    result = ''
    size = len(signal)
    half = size // 2
    sum = 0
    for position in reversed(range(half, size)):
        sum = sum + int(signal[position])
        result += str(sum)[-1:]
    return ('x' * half) + result[::-1]
    
def apply_pattern(signal, debug = False):
    result = ''
    size = len(signal)
    for repeat in range(0, size):
        if debug and repeat % 100 == 0:
            print '{}/{}'.format(repeat, size)
        result += get_digit_value(signal, size, repeat + 1)
    return result

def run_basic_tests():
    tests = [
        [ '12345678', 1, '48226158' ],
        [ '12345678', 2, '34040438' ],
        [ '12345678', 3, '03415518' ],
        [ '12345678', 4, '01029498' ],
        [ '80871224585914546619083218645595', 100, '24176176' ],
        [ '19617804207202209144916044189917', 100, '73745418' ],
        [ '69317163492948606335995924319873', 100, '52432133' ]
    ]
    passes = 0
    for test in tests:
        [ init_signal, phases, expected ] = test
        signal = init_signal
        for phase in range(0, phases):
            signal = apply_pattern(signal)
        if signal[:8] == expected:
            passes = passes + 1
            print '{} / {}: Expected {}, passed.'.format(init_signal, phases, expected)
        else:
            print '{} / {}: Expected {}, but got {}!'.format(init_signal, phases, expected, signal[:8])
    print '{}/{} tests passed.'.format(passes, len(tests))

def run_full_signal_tests():
    tests = [
        [ '03036732577212944063491565474664', '84462026' ],
        [ '02935109699940807407585447034323', '78725270' ],
        [ '03081770884921959731165446850517', '53553731' ]
    ]
    passes = 0
    for test in tests:
        [ init_signal, expected ] = test
        signal = init_signal * 10000
        offset = int(signal[:7])
        for phase in range(0, 100):
            signal = apply_pattern_fast(signal)
        actual = signal[offset:offset+8]
        if actual == expected:
            passes = passes + 1
            print '{}: Expected {}, passed.'.format(init_signal, expected)
        else:
            print '{}: Expected {}, but got {}!'.format(init_signal, expected, actual)
    print '{}/{} tests passed.'.format(passes, len(tests))

run_basic_tests()
run_full_signal_tests()

init_signal = read_data_from_file('day16-input.txt')

signal = init_signal
for phase in range(0, 100):
    print 'Phase {}'.format(phase)
    signal = apply_pattern(signal)
print signal[:8]

offset = int(init_signal[:7])
signal = init_signal * 10000
for phase in range(0, 100):
    print 'Full Signal Phase {}'.format(phase)
    signal = apply_pattern_fast(signal)
print signal[offset:offset+8]
