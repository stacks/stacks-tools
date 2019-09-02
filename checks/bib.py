from functions import *
import config

my = config.localProject + "/my.bib"


def print_error_bib(error_text, line, line_nr):
	print "Error: " + error_text
	print line,
	print "gvim +{} my.bib".format(line_nr)
	print


types = {'BOOK', 'ARTICLE', 'INCOLLECTION', 'UNPUBLISHED', 'MISC', 'INPROCEEDINGS'}

references = []

def check_at(line, nr):
	ok = 0
	for type in types:
		if line.find(type) == 1:
			ok = 1
                        n = len(type)
	if not ok:
		print_error_bib('type not ok', line, nr)
	else:
		comma_location = line.find(',')
		if comma_location < 0:
			print_error_bib('missing comma', line, nr)
		else:
			if not comma_location + 2 == len(line):
				print_error_bib('extra character', line, nr)
		ref = line[n + 2 : -2]
		references.append(ref)


keys = {'AUTHOR', 'TITLE', 'JOURNAL', 'FJOURNAL', 'SHORTJOURNAL', 'VOLUME', 'YEAR', 'NUMBER', 'PAGES', 'EPRINT', 'EPRINTTYPE', 'PUBLISHER', 'URL', 'SERIES', 'ADDRESS', 'CODEN', 'ISSN', 'NOTE', 'HOWPUBLISHED', 'EDITOR', 'CITY', 'ISBN', 'EDITION', 'CHAPTER', 'MONTH'}

def check_key_value(line, nr):
	ok = 0
	for key in keys:
		if line.find(key) >= 0:
			ok = 1
	if not ok:
		print_error_bib('key not ok', line, nr)

	a = 0
	for c in line:
		if c == '{': a = a + 1
		if c == '}': a = a - 1
	if not a == 0:
		print_error_bib('Problem with brackets!', line, nr)


bib_file = open(my, 'r')
nr = 0
previous_empty = 0
for line in bib_file:
	nr = nr + 1
	if line.find('%') == 0:
		continue
	if line.find('@') > 0:
		print_error_bib('@ in wrong spot', line, nr)
	if line.find('@') == 0:
		check_at(line, nr)
		continue
	if line.find('=') >= 0:
		check_key_value(line, nr)
	
bib_file.close()


def check_citations(line, name, nr):
	refs = []
	n = line.find("\\cite")
	while n >= 0:
		if line[n + 5] == '[':
			n = find_sub_clause(line, n + 5, "[", "]") + 1
		else:
			n = n + 5
		if not line[n] == '{':
			print_error('Incorrect citation!', line, name, nr)
			return
		m = find_sub_clause(line, n, "{", "}")
		ref = line[n + 1: m]
		if not ref in references:
			print_error('Citation wrong!', line, name, nr)
		n = line.find("\\cite", m)
	return refs

path = config.localProject + "/"

lijstje = list_text_files(path)

for name in lijstje:
	if name == "fdl": continue
	if name == "coding": continue
	tex_file = open(path + name + ".tex", 'r')
	nr = 0
	for line in tex_file:
		nr = nr + 1
		if line.find('\\cite') >= 0:
			check_citations(line, name, nr)
	
	tex_file.close()
