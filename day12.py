import math

class Moon:

    def __init__(self, x = 0, y = 0, z = 0, dx = 0, dy = 0, dz = 0):
        self.repeat_x = []
        self.repeat_y = []
        self.repeat_z = []
        self.step = 0
        self.init_x = x
        self.init_y = y
        self.init_z = z
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def __str__(self):
        return 'pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>'.format(self.x, self.y, self.z, self.dx, self.dy, self.dz)

    def __repr__(self):
        return 'Moon(pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>)'.format(self.x, self.y, self.z, self.dx, self.dy, self.dz)

    def shortstr(self):
        return '{},{},{}:{},{},{}'.format(self.x, self.y, self.z, self.dx, self.dy, self.dz)

    def get_gravity(self, other):
        return [ cmp(other.x, self.x), cmp(other.y, self.y), cmp(other.z, self.z) ]
    
    def get_total_gravity(self, others):
        total_gravity = [ 0, 0, 0 ]
        for other in others:
            gravity = self.get_gravity(other)
            total_gravity[0] = total_gravity[0] + gravity[0]
            total_gravity[1] = total_gravity[1] + gravity[1]
            total_gravity[2] = total_gravity[2] + gravity[2]
        return total_gravity

    def apply_gravity(self, gravity):
        self.dx = self.dx + gravity[0]
        self.dy = self.dy + gravity[1]
        self.dz = self.dz + gravity[2]

    def apply_velocity(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.z = self.z + self.dz
        self.step = self.step + 1
        if self.x == self.init_x and self.dx == 0:
            self.repeat_x.append(self.step)
        if self.y == self.init_y and self.dy == 0:
            self.repeat_y.append(self.step)
        if self.z == self.init_z and self.dz == 0:
            self.repeat_z.append(self.step)

    def repeat_dim(self, dim):
        if len(dim) < 2:
            return 0
        for i in range(0, len(dim) - 1):
            for j in range(i + 1, len(dim)):
                if dim[i] * 2 == dim[j]:
                    return dim[i]
        return 0

    def repeat_x_value(self):
        return self.repeat_dim(self.repeat_x)

    def repeat_y_value(self):
        return self.repeat_dim(self.repeat_y)

    def repeat_z_value(self):
        return self.repeat_dim(self.repeat_z)

    def is_complete(self):
        return self.repeat_x_value() > 0 and self.repeat_y_value() > 0 and self.repeat_z_value() > 0

def lcm(numbers):
    all_factors = {}
    for number in numbers:
        if not all_factors.has_key(number):
            factors = []
            root = int(math.floor(math.sqrt(number)))
            dividend = 2
            base = number
            while dividend <= number:
                while base % dividend == 0:
                    base = base / dividend
                    factors.append(dividend)
                dividend = dividend + 1
            all_factors[number] = factors
            print "Factors of {}: {}".format(number, factors)
    factor_counts = {}
    distinct_numbers = all_factors.keys()
    for number in distinct_numbers:
        for factor in all_factors[number]:
            count = all_factors[number].count(factor)
            if not factor_counts.has_key(factor) or factor_counts[factor] < count:
                factor_counts[factor] = count
                print 'number of occurrences of {}: {}'.format(factor, count)
    common_factors = []
    for factor in factor_counts.keys():
        for count in range(0, factor_counts[factor]):
            common_factors.append(factor)
    lcm_value = 1
    for factor in common_factors:
        lcm_value = lcm_value * factor
    print 'LCM: {} -> {}'.format(common_factors, lcm_value)
    return lcm_value

# moons = [
#     Moon(-1, 0, 2),
#     Moon(2, -10, -7),
#     Moon(4, -8, 8),
#     Moon(3, 5, -1)
# ]

# moons = [
#     Moon(-8, -10, 0),
#     Moon(5, 5, 10),
#     Moon(2, -7, 3),
#     Moon(9, -8, -3)
# ]

moons = [
    Moon(-1, -4, 0),
    Moon(4, 7, -1),
    Moon(-14, -10, 9),
    Moon(1, 2, 17)
]

step = 0

complete = False
while not complete:
    gravities = {}
    for moon in moons:
        print str(moon)
        gravities[moon] = moon.get_total_gravity(moons)
    complete = True
    for moon in moons:
        moon.apply_gravity(gravities[moon])
        moon.apply_velocity()
        complete = complete and moon.is_complete()
    step = step + 1

print 'Step {}: complete'.format(step)
repeats = []
for moon in moons:
    print 'repeat_x: {} = {}'.format(moon.repeat_x, moon.repeat_x_value())
    print 'repeat_y: {} = {}'.format(moon.repeat_y, moon.repeat_y_value())
    print 'repeat_z: {} = {}'.format(moon.repeat_z, moon.repeat_z_value())
    repeats.append(moon.repeat_x_value())
    repeats.append(moon.repeat_y_value())
    repeats.append(moon.repeat_z_value())
print 'LCM of {} is {}'.format(repeats, lcm(repeats))

# print "After {} steps:".format(total_steps)
# total_energy = 0
# for moon in moons:
#     print str(moon)
#     potential_energy = abs(moon.x) + abs(moon.y) + abs(moon.z)
#     kinetic_energy = abs(moon.dx) + abs(moon.dy) + abs(moon.dz)
#     moon_energy = potential_energy * kinetic_energy
#     total_energy = total_energy + moon_energy
#     print 'pot: {} + {} + {} = {}; kin: {} + {} + {} = {}; total: {} * {} = {}'.format(
#         abs(moon.x), abs(moon.y), abs(moon.z), potential_energy,
#         abs(moon.dx), abs(moon.dy), abs(moon.dz), kinetic_energy,
#         potential_energy, kinetic_energy, moon_energy)
# print 'Sum of total energy: {}'.format(total_energy)
