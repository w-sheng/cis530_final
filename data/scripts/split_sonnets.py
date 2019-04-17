
sonnet_length = 14

with open('sonnets.txt', 'r') as file:
	all_sonnets = file.read()
	list_of_sonnets = all_sonnets.split('\n\n')
	list_of_sonnets = list(filter(lambda x : len(x.strip()) > 0, list_of_sonnets)) 

	num_sonnets = len(list_of_sonnets)
	num_test = num_sonnets // 10
	num_dev = num_sonnets // 10
	num_train = num_sonnets - num_test - num_dev

with open('sonnets_test.txt', 'w') as file:
	for sonnet in list_of_sonnets[:num_test]:
		file.write(sonnet + '\n\n')

with open('sonnets_dev.txt', 'w') as file:
	for sonnet in list_of_sonnets[num_test:num_test + num_dev]:
		file.write(sonnet + '\n\n')

with open('sonnets_train.txt', 'w') as file:
	for sonnet in list_of_sonnets[num_test + num_dev:]:
		file.write(sonnet + '\n\n')