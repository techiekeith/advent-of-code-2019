first_number = 137683;
last_number = 596253;

def is_candidate_password(x):
	two_same = 0
	increasing = 0
	for i in range(0, 5):
		if (x[i] == x[i + 1] and (i == 0 or x[i] != x[i - 1]) and (i == 4 or x[i] != x[i + 2])):
			two_same = two_same + 1
		if x[i] <= x[i + 1]:
			increasing = increasing + 1
	return two_same >= 1 and increasing == 5

for i in range(first_number, last_number):
	a = str(i)
	if (is_candidate_password(a)):
		print a

