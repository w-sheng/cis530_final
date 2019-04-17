
sonnet_length = 14

with open('raw_sonnets.txt', 'r') as file:
	with open('sonnets.txt', 'w') as output:
		in_sonnet = False
		current_line = 1
		for line in file:
			if in_sonnet:
				line = line.strip()
				if current_line == 5:
					line = line[:-1].strip()
				elif current_line in [10, 14]:
					line = line[:-2].strip()
				output.write(line + '\n')
				current_line += 1
				if current_line > 14:
					in_sonnet = False
					current_line = 1
					output.write('\n')
			else:
				if len(line) > 6 and line[0:6] == 'SONNET':
					in_sonnet = True