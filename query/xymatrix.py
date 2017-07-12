import config
from functions import *

path = config.localProject + "/"

lijstje = list_text_files(path)

def begin_xymatrix(line):
	n = line.find("\\xymatrix{")
	if n > 0:
		raise Exception('\\xymatrix{ not at start of line.')
	if n == 0:
		return 1
	else:
		return 0

def nr_braces(text):
	spot = 0
	nr_braces = 0
	while spot < len(text):
		if text[spot] == '{':
			nr_braces = nr_braces + 1
		if text[spot] == '}':
			nr_braces = nr_braces - 1
		spot = spot + 1
	return nr_braces

ext = ".tex"
for name in lijstje:
	filename = path + name + ext
	tex_file = open(filename, 'r')
	line_nr = 0
	verbatim = 0
	xymatrix = 0
	xytext = ""
	for line in tex_file:

		# Update line number
		line_nr = line_nr + 1

		# Check for verbatim, because we do not check correctness
		# inside verbatim environment.
		verbatim = verbatim + beginning_of_verbatim(line)
		if verbatim:
			if end_of_verbatim(line):
				verbatim = 0
			continue

		# Check xymatrix
		xymatrix = xymatrix + begin_xymatrix(line)
		if not xymatrix:
			continue

		xytext = xytext + " " + line.rstrip()
		if nr_braces(xytext) == 0:
			xymatrix = 0
			print xytext
			xytext = ""

	tex_file.close()
