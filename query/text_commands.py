import config
from functions import *

path = config.localProject + "/"

text_commands = {}

lijstje = list_text_files(path)

# Silly function to detect commands of the form
#
# \abc{cde}
#
def find_text_commands(line):
	S = "( \\{_\n$[,'}])^/=.|+-:&\"@;"
	commands = []
	n = line.find("\\")
	while n >= 0:
		m = n + 1
		while m < len(line):
			if line[m].isalpha() == False:
				break
			m = m + 1
		if m > n + 1 and line[m] == '{':
			m = m + 1
			while m < len(line):
				if line[m].isalpha() == False:
					break
				m = m + 1
			if line[m] == '}':
				commands.append(line[n : m + 1])
		n = line.find("\\", m)
	return commands


ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	line_nr = 0
	verbatim = 0
	def_text = ""
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

		# Check for verbatim, because we do not look for commands
		# inside verbatim environment.
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			continue

		potential_new = find_text_commands(line)
		n = 0
		while n < len(potential_new):
			if potential_new[n] in text_commands:
				text_commands[potential_new[n]] += 1
			else:
				text_commands[potential_new[n]] = 1
			n = n + 1

	tex_file.close()


for command in sorted(text_commands, key=text_commands.get):
	print command, text_commands[command]
