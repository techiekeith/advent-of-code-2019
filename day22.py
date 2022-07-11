import fileinput

class Deck:

    def __init__(self, commands, deck_size):
        self.commands = commands
        self.deck_size = deck_size
    
    def deal_into_new_stack(self, card, argument, reverse = False):
        return self.deck_size - card - 1

    def deal_with_increment(self, card, argument, reverse = False):
        if reverse:
            while card % argument != 0:
                card += self.deck_size
            return card / argument
        else:
            return (card * argument) % self.deck_size

    def cut(self, card, argument, reverse = False):
        return (card + argument if reverse else card - argument) % self.deck_size

    def parse_command(self, command):
        if command == 'deal into new stack':
            operation = self.deal_into_new_stack
            argument = 0
        elif command.startswith('deal with increment '):
            operation = self.deal_with_increment
            argument = int(command[20:])
        elif command.startswith('cut '):
            operation = self.cut
            argument = int(command[4:])
        return [ operation, argument ]

    def get_instructions(self):
        instructions = []
        for command in self.commands:
            instructions.append(self.parse_command(command))
        return instructions

    def get_position_of(self, card):
        # print "Initial card: {}".format(card)
        instructions = self.get_instructions()
        for [ operation, argument ] in instructions:
            card = operation(card, argument)
            # print "Card after {} {}: {}".format(operation, argument, card)
        return card

    def get_card_at(self, initial_position):
        # print "Initial position: {}".format(initial_position)
        position = initial_position
        instructions = list(reversed(self.get_instructions()))
        for [ operation, argument ] in instructions:
            position = operation(position, argument, True)
            # print "Position before {} {}: {}".format(operation, argument, position)
        return position

# Tests

deck = Deck(['deal with increment 7', 'deal into new stack', 'deal into new stack'], 10)
assert deck.get_position_of(0) == 0
assert deck.get_position_of(1) == 7
assert deck.get_position_of(2) == 4
assert deck.get_position_of(3) == 1
assert deck.get_position_of(4) == 8
assert deck.get_position_of(5) == 5
assert deck.get_position_of(6) == 2
assert deck.get_position_of(7) == 9
assert deck.get_position_of(8) == 6
assert deck.get_position_of(9) == 3
assert deck.get_card_at(0) == 0
assert deck.get_card_at(1) == 3
assert deck.get_card_at(2) == 6
assert deck.get_card_at(3) == 9
assert deck.get_card_at(4) == 2
assert deck.get_card_at(5) == 5
assert deck.get_card_at(6) == 8
assert deck.get_card_at(7) == 1
assert deck.get_card_at(8) == 4
assert deck.get_card_at(9) == 7

deck = Deck(['cut 6', 'deal with increment 7', 'deal into new stack'], 10)
assert deck.get_position_of(0) == 1
assert deck.get_position_of(1) == 4
assert deck.get_position_of(2) == 7
assert deck.get_position_of(3) == 0
assert deck.get_position_of(4) == 3
assert deck.get_position_of(5) == 6
assert deck.get_position_of(6) == 9
assert deck.get_position_of(7) == 2
assert deck.get_position_of(8) == 5
assert deck.get_position_of(9) == 8
assert deck.get_card_at(0) == 3
assert deck.get_card_at(1) == 0
assert deck.get_card_at(2) == 7
assert deck.get_card_at(3) == 4
assert deck.get_card_at(4) == 1
assert deck.get_card_at(5) == 8
assert deck.get_card_at(6) == 5
assert deck.get_card_at(7) == 2
assert deck.get_card_at(8) == 9
assert deck.get_card_at(9) == 6

deck = Deck(['deal with increment 7', 'deal with increment 9', 'cut -2'], 10)
assert deck.get_position_of(0) == 2
assert deck.get_position_of(1) == 5
assert deck.get_position_of(2) == 8
assert deck.get_position_of(3) == 1
assert deck.get_position_of(4) == 4
assert deck.get_position_of(5) == 7
assert deck.get_position_of(6) == 0
assert deck.get_position_of(7) == 3
assert deck.get_position_of(8) == 6
assert deck.get_position_of(9) == 9
assert deck.get_card_at(0) == 6
assert deck.get_card_at(1) == 3
assert deck.get_card_at(2) == 0
assert deck.get_card_at(3) == 7
assert deck.get_card_at(4) == 4
assert deck.get_card_at(5) == 1
assert deck.get_card_at(6) == 8
assert deck.get_card_at(7) == 5
assert deck.get_card_at(8) == 2
assert deck.get_card_at(9) == 9

deck = Deck([
    'deal into new stack', 'cut -2', 'deal with increment 7', 'cut 8', 'cut -4',
    'deal with increment 7', 'cut 3', 'deal with increment 9', 'deal with increment 3', 'cut -1'], 10)
assert deck.get_position_of(0) == 7
assert deck.get_position_of(1) == 4
assert deck.get_position_of(2) == 1
assert deck.get_position_of(3) == 8
assert deck.get_position_of(4) == 5
assert deck.get_position_of(5) == 2
assert deck.get_position_of(6) == 9
assert deck.get_position_of(7) == 6
assert deck.get_position_of(8) == 3
assert deck.get_position_of(9) == 0
assert deck.get_card_at(0) == 9
assert deck.get_card_at(1) == 2
assert deck.get_card_at(2) == 5
assert deck.get_card_at(3) == 8
assert deck.get_card_at(4) == 1
assert deck.get_card_at(5) == 4
assert deck.get_card_at(6) == 7
assert deck.get_card_at(7) == 0
assert deck.get_card_at(8) == 3
assert deck.get_card_at(9) == 6

# Rules for part 1 and 2

commands = []
for line in fileinput.input(files=('day22-input.txt')):
    commands.append(line.strip())

# Part 1

deck = Deck(commands, 10007)
print "Position of card 2019: {}".format(deck.get_position_of(2019))

# Part 2

deck_size = 119315717514047
repeat = 101741582076661

deck = Deck(commands, deck_size)

offset = deck.get_card_at(0)
multiplier = (deck.get_card_at(1) - offset) % deck_size

offsets = [ offset ]
multipliers = [ multiplier ]

offset = 0
multiplier = 1
check = repeat
while check != 0:
    bit = check % 2
    check = check // 2
    last_offset = offsets[-1]
    last_multiplier = multipliers[-1]
    if bit == 1:
        # a'(an+b) + b': a'an + a'b + b': offset a'b + b', mult a'a
        offset = (last_multiplier * offset + last_offset) % deck_size
        multiplier = (last_multiplier * multiplier) % deck_size
    next_offset = (last_offset * (last_multiplier + 1)) % deck_size
    next_multiplier = (last_multiplier * last_multiplier) % deck_size
    offsets.append(next_offset)
    multipliers.append(next_multiplier)
    print "Check: {} offset: {} multiplier: {}".format(check, next_offset, next_multiplier)

# Offset for [repeat] shuffles
print "Offset [{}]: {}".format(repeat, offset)

# Multiplier for [repeat] shuffles
print "Multiplier [{}]: {}".format(repeat, multiplier)

card_at_2020 = (offset + (multiplier * 2020)) % deck_size
print "Card at position 2020 [{}]: {}".format(repeat, card_at_2020)
