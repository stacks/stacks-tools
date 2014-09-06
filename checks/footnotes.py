from functions import *
import config
from functions import *


def check_footnote(line, m, name, nr):
	n = 0
	while n < len(line):
		if line[n] == '$':
			m = 1 - m
		elif (m == 1) and line.find('footnote', n) == n:
			print_error('Footnote in math mode', line, name, nr)
		n = n + 1
	return m

path = config.localProject + "/"

lijstje = list_text_files(path)

in_math_mode = 0

for name in lijstje:
	if name == "fdl": continue
	if name == "coding": continue
	tex_file = open(path + name + ".tex", 'r')
	nr = 0
	for line in tex_file:
		nr = nr + 1
		if line.find('$$') == 0:
			in_math_mode = 1 - in_math_mode
			continue
		in_math_mode = check_footnote(line, in_math_mode, name, nr)
	
	if in_math_mode == 1:
		print_error('End chapter in math mode', line, name, nr)
	
	tex_file.close()
