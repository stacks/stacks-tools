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
	if line.find('\\bibliography{my}') == 0: return 1
	if line.find('\\end{document}') == 0: return 1
	if line.find('\\title{') == 0: return 1
	if line.find('\\phantomsection') == 0: return 1
	if line.find('\\tableofcontents') == 0: return 1
	if line.find('\\maketitle') == 0: return 1
	if line.find('\\input{chapters}') == 0: return 1
	if line.find('\\input{preamble}') == 0: return 1
	return 0

for name in lijstje:
	if name == "fdl": continue
	tex_file = open(path + name + ".tex", 'r')
	nr = 0
	previous_empty = 0
	for line in tex_file:
		nr = nr + 1
		if line.find('%') == 0: continue
		if line.strip() == "":
			previous_empty = 1
		else:
			if previous_empty:
				if not ok_for_first_line(line):
					print name, nr, line
			previous_empty = 0
	tex_file.close()
