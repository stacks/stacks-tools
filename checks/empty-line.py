import config
from functions import *

path = config.localProject + "/"

lijstje = list_text_files(path)

def ok_for_first_line(line):
	if line.find('\\begin{') == 0: return 1
	if line.find('\\noindent') == 0: return 1
	if line.find('\\medskip\\noindent') == 0: return 1
	if line.find('\\section{') == 0: return 1
	if line.find('\\subsection{') == 0: return 1
	if line.find('\\subsubsection{') == 0: return 1
	if line.find('\\phantomsection') == 0: return 1
	if line.find('\\bibliography{my}') == 0: return 1
	if line.find('\\end{document}') == 0: return 1
	if line.find('\\title{') == 0: return 1
	if line.find('\\tableofcontents') == 0: return 1
	if line.find('\\maketitle') == 0: return 1
	if line.find('\\input{chapters}') == 0: return 1
	if line.find('\\input{preamble}') == 0: return 1
	return 0

def previous_should_be_empty(line):
	if line.find('noindent') >= 0: return 1
	for env in list_of_labeled_envs:
		if env == 'equation': continue
		if line.find('\\begin{' + env) == 0: return 1
	if line.find('\\begin{proof') == 0: return 1
	for part in list_parts:
		if line.find('\\' + part) == 0: return 1
	return 0

for name in lijstje:
	if name == "fdl": continue
	if name == "coding": continue
	tex_file = open(path + name + ".tex", 'r')
	nr = 0
	previous_empty = 0
	ended = 0
	for line in tex_file:
		nr = nr + 1
		if not previous_empty and previous_should_be_empty(line):
			print_error("Previous line not empty", line, name, nr)
		if line.find('%') == 0: continue
		if line.strip() == "":
			previous_empty = 1
		else:
			if previous_empty:
				if not ok_for_first_line(line):
					print_error("Bad first line", line, name, nr)
				if ended and line.find('\\medskip\\noindent') == 0:
					print_error("Misplaced medskip", line, name, nr)
				ended = 0
			previous_empty = 0
			if line.find('\\end{') == 0:
				ended = 1
			else:
				ended = 0
	tex_file.close()
