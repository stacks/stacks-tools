from functions import *
import config
from functions import *
from sys import argv

exclude = []
n = 1
while n < len(argv):
	exclude.append(argv[n])
	n = n + 1

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


specials = [\
'\\{',\
'\\}',\
'\\ ',\
'\\hole ',\
'\\choose ',\
'\\vec{',\
'\\widehat{',\
'\\widetilde{',\
'\\widetilde M',\
'\\widetilde N',\
'\\widetilde R',\
'\\widetilde S',\
'\\widetilde I',\
'\\widetilde A',\
'\\widetilde B',\
'\\widetilde K',\
'\\linebreak[0]',\
'\\phantom{',\
'\\fbox{',\
'\\boxed{',\
'\\mod ',\
'\\bmod ',\
'\\gcd(',\
'\\check{C}',\
'\\check C',\
'\\check{\mathcal{C}}',\
'\\check{H}',\
'\\check H',\
'\\check \\xi',\
'\\ref{',\
'\\frac{',\
'\\overset{',\
'\\sqrt{',\
'\\stackrel{',\
'\\textstyle{',\
'\\binom{',\
'\\xrightarrow{',\
'\\xleftarrow{',\
'\\vcenter{',\
'\\xymatrix{',\
'\\xymatrix@',\
'\\xymatrix @',\
'\\label{equation-']

commands_in_math_mode = [\
'\\nonumber',\
'\\partial',\
'\\dagger',\
'\\!',\
'\\#',\
'\\natural',\
'\\sharp',\
'\\bullet',\
'\\prime',\
'\\text',\
'\\textit',\
'\\mathcal',\
'\\mathbf',\
'\\mathfrak',\
'\\mathit',\
'\\bar',\
'\\overline',\
'\\underline',\
'\\ldots',\
'\\cdot',\
'\\circ',\
'\\star',\
'\\diamond',\
'\\ast',\
'\\ell',\
'\\times',\
'\\otimes',\
'\\bigotimes',\
'\\wedge',\
'\\vee',\
'\\pm',\
'\\lfloor',\
'\\rfloor',\
'\\lceil',\
'\\rceil',\
'\\langle',\
'\\rangle',\
'\\hat',\
'\\tilde',\
'\\cup',\
'\\bigcup',\
'\\cap',\
'\\bigcap',\
'\\setminus',\
'\\mid',\
'\\sum',\
'\\quad',\
'\\prod',\
'\\coprod',\
'\\nolimits',\
'\\limits',\
'\\subset',\
'\\supset',\
'\\in',\
'\\notin',\
'\\to',\
'\\leadsto',\
'\\mapsto',\
'\\uparrow',\
'\\downarrow',\
'\\Leftrightarrow',\
'\\leftrightarrow',\
'\\longleftrightarrow',\
'\\longleftarrow',\
'\\leftarrow',\
'\\Leftarrow',\
'\\hookrightarrow',\
'\\rightarrow',\
'\\Rightarrow',\
'\\longrightarrow',\
'\\longmapsto',\
'\\begin{matrix}',\
'\\end{matrix}',\
'\\rtwocell',\
'\\rruppertwocell',\
'\\rrlowertwocell',\
'\\rrtwocell',\
'\\ll',\
'\\gg',\
'\\ge',\
'\\geq',\
'\\leq',\
'\\le',\
'\\not',\
'\\ne',\
'\\neq',\
'\\cong',\
'\\equiv',\
'\\sim',\
'\\simeq',\
'\\oplus',\
'\\bigoplus',\
'\\amalg',\
'\\lim',\
'\\colim',\
'\\emptyset',\
'\\infty',\
'\\dim',\
'\\deg',\
'\\det',\
'\\sup',\
'\\min',\
'\\max',\
'\\forall',\
'\\exists',\
'\\alpha',\
'\\beta',\
'\\gamma',\
'\\Gamma',\
'\\delta',\
'\\Delta',\
'\\epsilon',\
'\\varepsilon',\
'\\zeta',\
'\\eta',\
'\\theta',\
'\\vartheta',\
'\\iota',\
'\\kappa',\
'\\lambda',\
'\\Lambda',\
'\\mu',\
'\\nu',\
'\\xi',\
'\\Xi',\
'\\pi',\
'\\Pi',\
'\\rho',\
'\\sigma',\
'\\Sigma',\
'\\tau',\
'\\upsilon',\
'\\phi',\
'\\Phi',\
'\\varphi',\
'\\chi',\
'\\psi',\
'\\Psi',\
'\\omega',\
'\\Omega',\
'\\aleph',\
'\\Mor',\
'\\Hom',\
'\\SheafHom',\
'\\Sch',\
'\\Spec',\
'\\Ob',\
'\\Im',\
'\\Ker',\
'\\Coker',\
'\\Coim',\
'\\Sh',\
'\\QCoh',\
'\\NL',\
'\\etale']

open_braces = ['\\{', '(', '[', '.']
close_braces = ['\\}', ')', ']', '.']
bigs = ['\\Big', '\\big']
middles = ['\{', '\}', '/', '(', ')']

chars_after = '()\\,{} _$\n.^|\'/[]'

def command_allowed_in_math_mode(line, n):
	for special in specials:
		if line.find(special, n) == n:
			return 1
	for command in commands_in_math_mode:
		for c in chars_after:
			if line.find(command + c, n) == n:
				return 1
	if line.find('\\ar[', n) == n or line.find('\\ar@', n) == n or line.find('\\ar ', n) == n:
		return 1
	for brace in open_braces:
		if line.find('\\left' + brace, n) == n:
			return 1
	for brace in close_braces:
		if line.find('\\right' + brace, n) == n:
			return 1
	for big in bigs:
		for middle in middles:
			if line.find(big + middle, n ) == n:
				return 1
	return 0

def check_line(line, m, name, nr):
	n = 0
	while n < len(line):
		if line[n] == '$':
			m = 1 - m
		else:
			if (m == 1):
				if line.find('\\\\\n', n) == n:
					n = n + 2
				if line.find('\\footnote{', n) == n:
					print_error('Footnote in math mode', line, name, nr)
				if line.find('\\', n) == n:
					if not command_allowed_in_math_mode(line, n):
						print_error('command in math mode', line, name, nr)

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
        if name in exclude: continue
        print name
        print
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
