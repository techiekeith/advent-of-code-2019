import fileinput
import math

filename = 'day14-input-test1.txt'

class Product:
    quantity = 0
    name = ''

    def __init__(self, product_string, ingredients = None):
        string_array = product_string.split(' ')
        self.quantity = int(string_array[0])
        self.name = string_array[1]
        self.ingredients = ingredients

    def __repr__(self):
        return 'Product({}x {}) <= {}'.format(self.quantity, self.name, self.ingredients)

def read_recipes_from_file(filename):
    recipes = {}
    for line in fileinput.input(files=(filename)):
        line = line.strip()
        [ ingredients, product ] = line.split(' => ')
        ingredients = list(map(Product, ingredients.split(', ')))
        product = Product(product, ingredients)
        print '{}'.format(product)
        recipes[product.name] = product
    return recipes

def calculate_ore_requirements(product_name, quantity_required, recipes, spare):
    if spare.has_key(product_name):
        spare_quantity = spare[product_name]
        if spare_quantity > quantity_required:
            spare[product_name] = spare_quantity - quantity_required
            print 'Using {}x spare {}'.format(quantity_required, product_name)
            return [ 0, spare ]
        else:
            del spare[product_name]
            print 'Using {}x spare {}'.format(spare_quantity, product_name)
            quantity_required = quantity_required - spare_quantity

    if product_name == 'ORE':
        print '{}x ORE required'.format(quantity_required)
        return [ quantity_required, spare ]

    if not recipes.has_key(product_name):
        print 'ERROR! Product {} not found in reaction list'.format(product_name)
        exit(1)
    
    print 'Calculating ORE requirements for {}x {}'.format(quantity_required, product_name)
    product = recipes[product_name]
    multiple = math.ceil(quantity_required / product.quantity)
    quantity_selected = product.quantity * multiple
    print 'Multiple: {}'.format(multiple)
    ore_required = 0
    for reagent in product.ingredients:
        print '{}x {} needs {}x {}'.format(quantity_selected, product_name, reagent.quantity * multiple, reagent.name)
        [ more_ore_required, spare ] = calculate_ore_requirements(reagent.name, reagent.quantity * multiple, recipes, spare)
        ore_required = ore_required + more_ore_required

    if quantity_selected > quantity_required:
        if not spare.has_key(product_name):
            spare[product_name] = 0
        spare[product_name] = spare[product_name] + quantity_selected - quantity_required

    print 'ORE required for {}x {}: {} - spare: {}'.format(quantity_required, product_name, ore_required, spare)
    return [ ore_required, spare ]

def calculate_fuel_requirements(recipes):
    return calculate_ore_requirements('FUEL', 1, recipes, {})

def calculate_fuel_produced_by_trillion_units_of_ore(recipes):
    spare_ore = 1000000000000
    [ ore_required_for_one_fuel, junk ] = calculate_ore_requirements('FUEL', 1, recipes, {})
    fuel_estimate = spare_ore // ore_required_for_one_fuel
    fuel_produced = 0
    ore_required = 0
    while ore_required == 0:
        print 'Fuel estimate: {}'.format(fuel_estimate)
        [ ore_required, spare ] = calculate_ore_requirements('FUEL', fuel_estimate, recipes, { 'ORE': spare_ore })
        if ore_required == 0:
            ore_used_in_spare_ingredients = 0
            for product_name in spare:
                [ ore_required_for_spare, spare2 ] = calculate_ore_requirements(product_name, spare[product_name], recipes, {})
                ore_used_in_spare_ingredients = ore_used_in_spare_ingredients + ore_required_for_spare
            possible_extra_fuel = ore_used_in_spare_ingredients // ore_required_for_one_fuel
            if possible_extra_fuel == 0:
                possible_extra_fuel = 1
            fuel_produced = fuel_estimate
            fuel_estimate = fuel_estimate + possible_extra_fuel
    return fuel_produced

def run_fuel_requirement_tests():
    expected_results = [ 31, 165, 13312, 180697, 2210736 ]
    passes = 0
    for i in range(0, len(expected_results)):
        filename = 'day14-input-test{}.txt'.format(i + 1)
        recipes = read_recipes_from_file(filename)
        [ ore_required, spare ] = calculate_fuel_requirements(recipes)
        result = 'SUCCESS' if ore_required == expected_results[i] else 'FAIL'
        print 'Test {}, ORE required expected {}, actual {}: {}'.format(i + 1, expected_results[i], ore_required, result)
        if result == 'SUCCESS':
            passes = passes + 1
    print '{}/{} tests passed.'.format(passes, len(expected_results))

def run_fuel_production_tests():
    expected_results = [ 82892753, 5586022, 460664 ]
    passes = 0
    for i in range(0, len(expected_results)):
        filename = 'day14-input-test{}.txt'.format(i + 3)
        recipes = read_recipes_from_file(filename)
        fuel_produced = calculate_fuel_produced_by_trillion_units_of_ore(recipes)
        result = 'SUCCESS' if fuel_produced == expected_results[i] else 'FAIL'
        print 'Test {}, FUEL produced expected {}, actual {}: {}'.format(i + 1, expected_results[i], fuel_produced, result)
        if result == 'SUCCESS':
            passes = passes + 1
    print '{}/{} tests passed.'.format(passes, len(expected_results))

run_fuel_requirement_tests()
run_fuel_production_tests()

recipes = read_recipes_from_file('day14-input.txt')
[ ore_required, spare ] = calculate_fuel_requirements(recipes)
print 'Ore required: {}'.format(ore_required)
fuel_produced = calculate_fuel_produced_by_trillion_units_of_ore(recipes)
print 'Fuel produced with a trillion units of ore: {}'.format(fuel_produced)
