import os

# invert a dictionary mapping
def invert_dict(dictionary):
  return dict((v, k) for k, v in dictionary.iteritems()) 

# return all files with a given extension
def list_files(path, extension):
  return filter(lambda filename: filename.endswith(extension), os.listdir(path))

# return all TeX files in a directory
def list_aux_files(path):
  return list_files(path, '.aux')

# return all TeX files in a directory
def list_tex_files(path):
  return list_files(path, '.tex')

# get the title from a TeX file
def get_chapter_title(path):
  tex_file = open(path, 'r')

  title = ''
  for line in tex_file:
    if line.startswith('\\title'):
      title = line[7:line.find('}')]
      break

  return title

# get the dictionary relating TeX files to their respective titles
def get_titles(path):
  titles = {}

  for tex_file in list_tex_files(path):
    titles[tex_file[0:-4]] = get_chapter_title(path + tex_file)

  return titles

# recursively find the filename of a section
def find_file_for_section(titles, sections, number):
  for section in sections:
    # found the correct section
    if section[1] == number:
      # it is a chapter, we can look it up
      if len(number.split('.')) == 1:
        return invert_dict(titles)[section[2]]
      # recurse
      else:
        return find_file_for_section(titles, sections, '.'.join(number.split('.')[0:-1]))

# get the information from a \contentsline macro in a .toc file
# This function should return
# [type, number, title, page number]
def parse_contentsline(contentsline):
  parts = contentsline.split('}{')

  # sanitize first element to determine type
  parts[0] = parts[0][15:]
  # remove clutter
  parts = map(lambda part: part.strip('{}'), parts)

  # currently the last part of a contents line for the bibliopgraphy
  # looks like 'chapter*.89}\n' and hence the following works for now
  if parts[3] == 'Bibliography':
    number = ''
    for i in parts[5]:
        if i.isdigit():
            number += i
    return [parts[0], number, parts[3], parts[4]]

  return [parts[0], parts[2], parts[3], parts[4]]

# read and extract all information from a .toc file
def parse_book_toc(filename):
  toc = open(filename, 'r')
  sections = [parse_contentsline(line)[0:4] for line in toc]
  toc.close()

  return sections

# get the information from a \newlabel macro in a .aux file
def parse_newlabel(newlabel):
  parts = newlabel.split('}{')

  # get the actual label
  parts[0] = parts[0][10:]
  # remove clutter
  parts = map(lambda part: part.strip('{}'), parts)

  # TODO document results
  return parts

# read and extract all information from a .aux file
def parse_aux(filename):
  aux = open(filename)

  labels = {}

  # counting the lines (useful for ordering the data)
  i = 0

  for line in aux:
    # not interesting, go to next line
    if not line.startswith("\\newlabel{"):
      continue

    parts = parse_newlabel(line)

    # not an actual label, just LaTeX layout bookkeeping, go to next line
    if len(parts) == 2:
      continue
    # it is a label, add it with what we already know about it
    else:
      if parts[3].endswith("\\relax "):
        parts[3] = parts[3][0:-7]
      labels[parts[0]] = (parts[1], parts[2], parts[3], parts[0].partition('-')[0], i)
      i = i + 1

  return labels

list_of_standard_envs = ['abstract', 'verbatim', 'quote', 'itemize', 'list', 'center', 'eqnarray*', 'eqnarray', 'align', 'align*', 'document', 'enumerate', 'proof', 'matrix', 'lemma', 'proposition', 'theorem', 'remark', 'remarks', 'example', 'exercise', 'situation', 'equation', 'definition', 'item', 'reference', 'slogan', 'history']

# We also have labels for
#	'section', 'subsection', 'subsubsection' (every one of these has a label)
#	'item' (typically an item does not have a label)
list_of_labeled_envs = ['lemma', 'proposition', 'theorem', 'remark', 'remarks', 'example', 'exercise', 'situation', 'equation', 'definition']

list_parts = ['section', 'subsection', 'subsubsection', 'phantomsection']

list_of_proof_envs = ['lemma', 'proposition', 'theorem']

list_of_standard_labels = ['definition', 'lemma', 'proposition', 'theorem', 'remark', 'remarks', 'example', 'exercise', 'situation', 'equation', 'section', 'subsection', 'subsubsection', 'item']

# Get file name
def get_name():
	from sys import argv
	if not len(argv) == 2:
		print
		print "This script needs exactly one argument"
		print "namely the path to the file"
		print
		raise Exception('Wrong arguments')
	name = argv[1]
	return name

# List the stems of the TeX files in the project
# in the correct order
def list_text_files(path):
	Makefile_file = open(path + "Makefile", 'r')
	for line in Makefile_file:
		n = line.find("LIJST = ")
		if n == 0:
			break
	lijst = ""
	while line.find("\\") >= 0:
		line = line.rstrip()
		line = line.rstrip("\\")
		lijst = lijst + " " + line
		line = Makefile_file.next()
	Makefile_file.close()
	lijst = lijst + " " + line
	lijst = lijst.replace("LIJST = ", "")
	lijst = lijst + " fdl"
	return lijst.split()

# Print error
def print_error(error_text, line, name, line_nr):
	print "In file " + name + ".tex on line", line_nr
	print line.rstrip()
	print "Error: " + error_text
	print "gvim +{} {}.tex".format(line_nr, name)
	print

# Check length line
def length_of_line(line):
	n = len(line)
	if n > 81:
		return "More than 80 characters on a line."
	return ""

# Check if line starts with given pattern
def beginning_of_line(pattern, line):
	n = line.find(pattern)
	if n > 0:
		return "Pattern: " + pattern + " not at the start of the line."
	return ""

# See if line starts an environment
def beginning_of_env(line):
	n = line.find("\\begin{")
	if n == 0:
		return 1
	return 0

# See if line starts a definition
def beginning_of_definition(line):
	n = line.find("\\begin{definition}")
	if n == 0:
		return 1
	return 0

# See if line ends a definition
def end_of_definition(line):
	n = line.find("\\end{definition}")
	if n == 0:
		return 1
	return 0

# See if line starts a proof
def beginning_of_proof(line):
	n = line.find("\\begin{proof}")
	if n == 0:
		return 1
	return 0

# See if line ends a proof
def end_of_proof(line):
	n = line.find("\\end{proof}")
	if n == 0:
		return 1
	return 0

# See if line starts verbatim environment,
# also check if the \begin{verbatim} starts the line
def beginning_of_verbatim(line):
	n = line.find("\\begin{verbatim}")
	if n > 0:
		raise Exception('\\begin{verbatim} not at start of line.')
	if n == 0:
		return 1
	else:
		return 0

# See if line ends verbatim environment,
# also check if the \begin{verbatim} starts the line
def end_of_verbatim(line):
	n = line.find("\\end{verbatim}")
	if n > 0:
		raise Exception('\\end{verbatim} not at start of line.')
	if n == 0:
		return 1
	return 0

# Find clause starting in specific spot with specific open and close characters
def find_sub_clause(text, spot, open, close):
	nr_braces = 0
	while nr_braces >= 0:
		spot = spot + 1
		if text[spot] == open:
			nr_braces = nr_braces + 1
		if text[spot] == close:
			nr_braces = nr_braces - 1
	return spot

# See if there is a clause immediately following the current spot, and
# return spot of closing brace
def next_clause(text, spot):
	open = ""
	if spot + 1 == len(text):
		return spot
	if text[spot + 1] == "[":
		open = "["
		close = "]"
	if text[spot + 1] == "{":
		open = "{"
		close = "}"
	if open:
		spot = find_sub_clause(text, spot + 1, open, close)
	return spot

# Find spot of last brace of sequence of clauses starting at spot
def rest_clauses(text, spot):
	n = next_clause(text, spot)
	while n > spot:
		spot = n
		n = next_clause(text, spot)
	return n

# Check if the pattern starts the line and has only clauses following...
def only_on_line(pattern, spot, line):
	n = line.find(pattern)
	if n > 0:
		return "Pattern: " + pattern + "not at the start of the line."
	if n == 0:
		m = find_sub_clause(line, spot, "{", "}")
		m = rest_clauses(line, m)
		if not m + 2 == len(line):
			return "Pattern: " + pattern + "*} not by itself."
	return ""

# Check if $$ is by itself and at the start of the line
def check_double_dollar(line):
	n = line.find("$$")
	if n < 0:
		return ""
	if n > 0:
		return "Double dollar not at start of line."
	if not len(line) == 3:
		return "Double dollar not by itself on line."

# Check if the line contains the title of the document
def is_title(line):
	n = line.find("\\title{")
	if n < 0:
		return 0
	return 1

# Returns short label. Does not assume there is a label on the line
def find_label(env_text):
	n = env_text.find("\\label{")
	if n < 0:
		return ""
	n = n + 6
	m = find_sub_clause(env_text, n, "{", "}")
	label = env_text[n + 1 : m]
	return label

# Returns list of full references on the line
def find_refs(line, name):
	refs = []
	n = line.find("\\ref{")
	while n >= 0:
		m = find_sub_clause(line, n + 4, "{", "}")
		ref = line[n + 5: m]
		if standard_label(ref):
			ref = name + "-" + ref
		refs.append(ref)
		n = line.find("\\ref{", m)
	return refs

# Check if short label is standard
def standard_label(label):
	n = 0
	while n < len(list_of_standard_labels):
		if label.find(list_of_standard_labels[n] + '-') == 0:
			return 1
		n = n + 1
	return 0

# Split label into components
def split_label(label):
	pieces = label.split('-')
	name = pieces[0]
	type = pieces[1]
	rest = ""
	n = 2
	# TODO We should automate this...
	if name == "more" and type == "algebra":
		name = "more-algebra"
		type = pieces[2]
		n = 3
	if name == "sites" and type == "modules":
		name = "sites-modules"
		type = pieces[2]
		n = 3
	if name == "sites" and type == "cohomology":
		name = "sites-cohomology"
		type = pieces[2]
		n = 3
	if name == "more" and type == "morphisms":
		name = "more-morphisms"
		type = pieces[2]
		n = 3
	if name == "more" and type == "groupoids":
		name = "more-groupoids"
		type = pieces[2]
		n = 3
	if name == "etale" and type == "cohomology":
		name = "etale-cohomology"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "properties":
		name = "spaces-properties"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "morphisms":
		name = "spaces-morphisms"
		type = pieces[2]
		n = 3
	if name == "decent" and type == "spaces":
		name = "decent-spaces"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "cohomology":
		name = "spaces-cohomology"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "limits":
		name = "spaces-limits"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "divisors":
		name = "spaces-divisors"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "over" and pieces[2] == "fields":
		name = "spaces-over-fields"
		type = pieces[3]
		n = 4
	if name == "spaces" and type == "topologies":
		name = "spaces-topologies"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "descent":
		name = "spaces-descent"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "perfect":
		name = "spaces-perfect"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "more" and pieces[2] == "morphisms":
		name = "spaces-more-morphisms"
		type = pieces[3]
		n = 4
        if name == "spaces" and type == "pushouts":
                name = "spaces-pushouts"
                type = pieces[2]
                n = 3
	if name == "spaces" and type == "groupoids":
		name = "spaces-groupoids"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "more" and pieces[2] == "groupoids":
		name = "spaces-more-groupoids"
		type = pieces[3]
		n = 4
	if name == "groupoids" and type == "quotients":
		name = "groupoids-quotients"
		type = pieces[2]
		n = 3
	if name == "spaces" and type == "simplicial":
		name = "spaces-simplicial"
		type = pieces[2]
		n = 3
	if name == "formal" and type == "spaces":
		name = "formal-spaces"
		type = pieces[2]
		n = 3
	if name == "formal" and type == "defos":
		name = "formal-defos"
		type = pieces[2]
		n = 3
	if name == "examples" and type == "stacks":
		name = "examples-stacks"
		type = pieces[2]
		n = 3
	if name == "stacks" and type == "sheaves":
		name = "stacks-sheaves"
		type = pieces[2]
		n = 3
	if name == "stacks" and type == "properties":
		name = "stacks-properties"
		type = pieces[2]
		n = 3
	if name == "stacks" and type == "morphisms":
		name = "stacks-morphisms"
		type = pieces[2]
		n = 3
	if name == "stacks" and type == "cohomology":
		name = "stacks-cohomology"
		type = pieces[2]
		n = 3
	if name == "stacks" and type == "perfect":
		name = "stacks-perfect"
		type = pieces[2]
		n = 3
	if name == "stacks" and type == "introduction":
		name = "stacks-introduction"
		type = pieces[2]
		n = 3
	while n < len(pieces):
		rest = rest + "-" + pieces[n]
		n = n + 1
	return [name, type, rest]

# Check if environment is standard
# The input should be a line from latex file containing the
# \begin{environment} statement
def standard_env(env):
	n = 0
	while n < len(list_of_standard_envs):
		if env.find('{' + list_of_standard_envs[n] + '}') >= 0:
			return 1
		n = n + 1
	return 0

# Check if environment should have a label
# The input should be a line from latex file containing the
# \begin{environment} statement
def labeled_env(env):
	n = 0
	while n < len(list_of_labeled_envs):
		if env.find('\\begin{' + list_of_labeled_envs[n] + '}') == 0:
			return 1
		n = n + 1
	return 0

def end_labeled_env(env):
	n = 0
	while n < len(list_of_labeled_envs):
		if env.find('\\end{' + list_of_labeled_envs[n] + '}') == 0:
			return 1
		n = n + 1
	return 0

# Check for start of new part
def new_part(line):
	n = 0
	while n < len(list_parts):
		if line.find('\\' + list_parts[n]) == 0:
			return 1
		n = n + 1
	return 0

# Check for start of new item
def new_item(line):
	if line.find('\\item') == 0:
		return 1
	return 0

# Check if environment should have a proof
# The input should be a line from latex file containing the
# \begin{environment} statement
def proof_env(env):
	n = 0
	while n < len(list_of_proof_envs):
		if env.find('{' + list_of_proof_envs[n] + '}') >= 0:
			return 1
		n = n + 1
	return 0

# Checks inner text of definition for existence of a label (this is now
# obsolete) and for the existence of at least one term which is being
# defined
def check_def_text(def_text):
	n = def_text.find("\\label{")
	if n < 0:
		return "No label in definition."
	n = def_text.find("{\\it ")
	if n < 0:
		return "Nothing defined in definition."
	return ""

# See if ref occurs in list labels
def check_ref(ref, labels):
	try:
		labels.index(ref)
	except:
		return 0
	return 1

# See if references on line are internal
# this uses that the references have the correct shape
def internal_refs(line, refs, name):
	n = 0
	while n < len(refs):
		ref = refs[n]
		split = split_label(ref)
		if name == split[0] and line.find(ref) >= 0:
			return ref
		n = n + 1
	return ""

# See if references already occur in list labels
def check_refs(refs, labels):
	n = 0
	while n < len(refs):
		ref = refs[n]
		if ref == "":
			return "empty reference"
		if not check_ref(ref, labels):
			return ref
		n = n + 1
	return ""

# Silly function to detect LaTeX commands. Not perfect.
def find_commands(line):
	S = "( \\{_\n$[,'}])^/=.|+-:&\"@;"
	commands = []
	n = line.find("\\")
	while n >= 0:
		m = n + 1
		while m < len(line):
			if S.find(line[m]) >= 0:
				break
			m = m + 1
		if m == n + 1:
			m = m + 1
		commands.append(line[n : m])
		n = line.find("\\", m)
	return commands

# See if a command already occurs
def new_command(new, commands):
	try:
		commands.index(new)
	except:
		return 1
	return 0

# Silly function
def get_tag_line(line):
	line = line.rstrip()
	return line.split(",")

# Get all active tags in the project
def get_tags(path):
	tags = []
	tag_file = open(path + "tags/tags", 'r')
	for line in tag_file:
		if not line.find("#") == 0:
			tags.append(get_tag_line(line))
	tag_file.close()
	return tags

def new_label(tags, label):
	n = 0
	new = 1
	while new and n < len(tags):
		if tags[n][1] == label:
			new = 0
		n = n + 1
	return new

def cap_type(type):
	return type[0].capitalize() + type[1:]

