import fileinput
import sys

rows = 6
columns = 25
layer_size = rows * columns

image = ''
for line in fileinput.input(files=('day8-input.txt')):
    image = image + line.strip()

num_layers = len(image) // layer_size
print "Length: " + str(len(image)) + " (" + str(num_layers) + " layers)"

max_digits = 10
selected_layer = -1
digits_in_selected_layer = [ layer_size ]
for digit in range(1, max_digits):
    digits_in_selected_layer.append(0)

layers = []

for layer in range(0, num_layers):
    start = layer_size * layer
    end = start + layer_size
    layers.append(image[start:end])
    digits_in_this_layer = [ ]
    for digit in range(0, max_digits):
        digits_in_this_layer.append(0)
    for position in range(0, layer_size):
        digit = int(image[start + position])
        digits_in_this_layer[digit] = digits_in_this_layer[digit] + 1
    if digits_in_this_layer[0] < digits_in_selected_layer[0]:
        selected_layer = layer
        for digit in range(0, len(digits_in_selected_layer)):
            digits_in_selected_layer[digit] = digits_in_this_layer[digit]
    print "Layer " + str(layer) + ": " + str(digits_in_this_layer)

print "Selected layer: " + str(selected_layer) + ": " + str(digits_in_selected_layer)
print "1s x 2s: " + str(digits_in_selected_layer[1] * digits_in_selected_layer[2])

composite_layer = layers[num_layers - 1]

for layer_number in reversed(range(0, num_layers - 1)):
    layer = layers[layer_number]
    new_composite_layer = ''
    for position in range(0, layer_size):
        digit = layer[position]
        if digit == '2':
            digit = composite_layer[position]
        new_composite_layer = new_composite_layer + digit
    composite_layer = new_composite_layer

processed_image = ''
for digit in composite_layer:
    if digit == '1':
        processed_image = processed_image + '*'
    else:
        processed_image = processed_image + ' '

for row in range(0, rows):
    start = row * columns
    end = start + columns
    print processed_image[start:end]