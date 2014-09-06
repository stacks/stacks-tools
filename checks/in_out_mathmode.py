from functions import *
import config
from functions import *

commands_outside_math_mode = [\
'\\noindent',\
'\\ref{',\
'\\begin{',\
'\\end{',\
'\\label{',\
'\\item ',\
'\\item\n',\
'\\item[',\
'\\medskip',\
'\\section{',\
'\\subsection{',\
'\\subsubsection{',\
'\\romannumeral',\
'\\cite[',\
'\\cite{',\
'\\ ',\
'\\footnote{',\
'\\it ',\
'\\bf ',\
'\\title{',\
'\\input{chapters}',\
'\\tableofcontents',\
'\\maketitle',\
'\\input{preamble}',\
'\\phantomsection',\
'\\href{',\
'\\url{',\
'\\hyperref{',\
'\\hyperref[',\
'\\bibliography{my}',\
'\\bibliographystyle{amsalpha}',\
'\\emph{',\
'\\em ',\
'\\\'e',\
'\\`e',\
'\\\'E',\
'\\v C',\
'\\`a',\
'\\\"a',\
'\\\"e',\
'\\\"o',\
'\\& ',\
'\\% ',\
'\\S ']

def command_allowed_outside_math_mode(line, n):
	for command in commands_outside_math_mode:
		if line.find(command, n) == n:
			return 1
	return 0

def check_line(line, m, name, nr):
	n = 0
	while n < len(line):
		if line[n] == '$':
			m = 1 - m
		else:
			if (m == 1) and line.find('footnote', n) == n:
				print_error('Footnote in math mode', line, name, nr)
			if (m == 0):
				if line.find('\\', n) == n:
					if not command_allowed_outside_math_mode(line, n):
						print_error('command in text', line, name, nr)
		n = n + 1
	return m

path = config.localProject + "/"

lijstje = list_text_files(path)

in_math_mode = 0
in_display_math_mode = 0

for name in lijstje:
	if name == "fdl": continue
	if name == "coding": continue
	tex_file = open(path + name + ".tex", 'r')
	nr = 0
	for line in tex_file:
		nr = nr + 1
		if line.find('$$') == 0 or line.find('{equation}') >= 0 or line.find('{align}') >= 0 or line.find('{align*}') >= 0 or line.find('{eqnarray}') >= 0 or line.find('{eqnarray*}') >= 0:
			in_math_mode = 1 - in_math_mode
                        in_display_math_mode = 1 - in_display_math_mode
			continue
                if in_display_math_mode and line.find('$') >= 0:
			print_error('Dollar in display math', line, name, nr)
		in_math_mode = check_line(line, in_math_mode, name, nr)
	
	if in_math_mode == 1:
		print_error('End chapter in math mode', line, name, nr)
	
	tex_file.close()
