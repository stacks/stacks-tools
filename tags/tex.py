from sys import exit
import sqlite3
from functions import *
import config, general
import re

"""
This is a modification of the original make_locate.py. It just (ab)uses the
existing code and inserts the corresponding TeX into the database. It would
be wise to:
  - refactor this
  - move this into the actual parsing of tags (the current set-up is not bad
    but isn't optimal I think)
"""

connection = 0

# Variable to contain all the texts of labels
label_texts = {}

# Variable to contain all the line numbers related to labels
label_linenumbers = {}

# Variable to contain all the texts of proofs
proof_texts = {}

# Variable to contain all the texts of references
reference_texts = {}

# Helper function
def assign_label_text(label, text):
    if not label:
        exit(1)
    if not text:
        print label
        exit(1)
    label_texts[label] = text

def assign_label_linenumbers(label, linenumbers):
    label_linenumbers[label] = list(linenumbers)

path = config.websiteProject + "/"

# Get all tags
tags = get_tags(path)
label_tags = dict((tags[n][1], tags[n][0]) for n in range(0, len(tags)))

lijstje = list_text_files(path)

# Function to convert refs into links
def make_links(line, name):
    new_line = ""
    m = 0
    n = line.find("\\ref{")
    while n >= 0:
        new_line = new_line + line[m : n + 5]
        m = find_sub_clause(line, n + 4, "{", "}")
        ref = line[n + 5: m]
        if standard_label(ref):
            label = name + "-" + ref
        else:
            label = ref
        if label in label_tags:
            new_line = new_line + '<a href="' + general.href('tag/' + label_tags[label]) + '\">' + ref + '</a>'
        else:
            new_line = new_line + ref
        n = line.find("\\ref{", m)
    new_line = new_line + line[m:]
    return new_line

# Get text of
#   labeled environments
#   proofs
#   labeled items
#   sections, subsections, subsubsections
#   equations
ext = ".tex"
for name in lijstje:
    filename = path + name + ext
    tex_file = open(filename, 'r')
    line_nr = 0
    verbatim = 0
    in_env = 0
    in_proof = 0
    in_item = 0
    in_section = 0
    in_subsection = 0
    in_subsubsection = 0
    in_equation = 0
    in_reference = 0
    label = ""
    label_env = ""
    label_proof = ""
    label_item = ""
    label_section = ""
    label_subsection = ""
    label_subsubsection = ""
    label_equation = ""
    label_reference = ""
    text_env = ""
    text_proof = ""
    text_item = ""
    text_section = ""
    text_subsection = ""
    text_subsubsection = ""
    text_equation = ""
    text_reference = ""

    linenumber_env = [1, 1]
    linenumber_proof = [1, 1]
    linenumber_item = [1, 1]
    linenumber_section = [1, 1]
    linenumber_subsection = [1, 1]
    linenumber_subsubsection = [1, 1]
    linenumber_equation = [1, 1]
    linenumber_reference = [1, 1]

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

        # See if labeled environment starts
        if labeled_env(line) and line.find("\\begin{equation}") < 0:
            in_env = 1
            linenumber_env[0] = line_nr

        # See if a proof starts
        if beginning_of_proof(line):
            in_proof = 1

        # See if item starts
        if new_item(line):
            # Closeout previous item
            if in_item and label_item:
                assign_label_text(label_item, text_item)
                linenumber_item[1] = line_nr
                assign_label_linenumbers(label_item, linenumber_item)

                in_item = 0
                text_item = ""
                label_item = ""

            in_item = 1
            linenumber_item[0] = line_nr

        # See if section starts
        if new_part(line):
            # Closeout previous section/subsection/subsubsection
            if in_section and line.find('\\section') == 0:
                assign_label_text(label_section, text_section)
                linenumber_section[1] = line_nr - 1
                assign_label_linenumbers(label_section, linenumber_section)

                in_section = 0
                text_section = ""
                label_section = ""
            if in_subsection and (line.find('\\section') == 0 or line.find('\\subsection') == 0):
                assign_label_text(label_subsection, text_subsection)
                linenumber_subsection[1] = line_nr - 1
                assign_label_linenumbers(label_subsection, linenumber_subsection)

                in_subsection = 0
                text_subsection = ""
                label_subsection = ""
            if in_subsubsection and (line.find('\\section') == 0 or line.find('\\subsection') == 0 or line.find('\\subsubsection') == 0):
                assign_label_text(label_subsubsection, text_subsubsection)
                linenumber_subsubsection[1] = line_nr - 1
                assign_label_linenumbers(label_subsubsection, linenumber_subsubsection)

                in_subsubsection = 0
                text_subsubsection = ""
                label_subsubsection = ""
            # Start new section/subsection/subsubsection
            if line.find('\\section') == 0:
                in_section = 1
                linenumber_section[0] = line_nr

            if line.find('\\subsection') == 0:
                in_subsection = 1
                linenumber_subsection[0] = line_nr

            if line.find('\\subsubsection') == 0:
                in_subsubsection = 1
                linenumber_subsubsection[0] = line_nr

        # See if equation starts
        if line.find('\\begin{equation}') == 0:
            linenumber_equation[0] = line_nr
            in_equation = 1

        # See if reference starts
        if line.find('\\begin{reference}') == 0:
            linenumber_reference[0] = line_nr
            in_reference = 1

        # Find label if there is one
        if line.find('\\label{') == 0:
            label = find_label(line)
            if label.find('item') == 0:
                label_item = name + '-' + label
            elif label.find('section') == 0:
                label_section = name + '-' + label
            elif label.find('subsection') == 0:
                label_subsection = name + '-' + label
            elif label.find('subsubsection') == 0:
                label_subsubsection = name + '-' + label
            elif label.find('equation') == 0:
                label_equation = name + '-' + label
            else:
                label_env = name + '-' + label
                if label.find('lemma') == 0 or label.find('proposition') == 0 or label.find('theorem') == 0:
                    label_proof = label_env
                    label_reference = label_env

        # Add line to env_text if we are in an environment
        if in_env:
            text_env = text_env + make_links(line, name)

        # Add line to proof_text if we are in a proof
        if in_proof:
            text_proof = text_proof + make_links(line, name)

        # Add line to item_text if we are in an item
        if in_item:
            text_item = text_item + make_links(line, name)

        # Add line to section_text if we are in a section
        if in_section:
            text_section = text_section + make_links(line, name)
        if in_subsection:
            text_subsection = text_subsection + make_links(line, name)
        if in_subsubsection:
            text_subsubsection = text_subsubsection + make_links(line, name)

        # Add line to equation_text if we are in an equation
        if in_equation:
            text_equation = text_equation + make_links(line, name)

        if in_reference:
            text_reference = text_reference + make_links(line, name)

        # Closeout env
        if end_labeled_env(line) and line.find("\\end{equation}") < 0:
            assign_label_text(label_env, text_env)
            linenumber_env[1] = line_nr # this is not perfect, as we do not take the proof into account, but it should be clear from the context where the proof is to be found
            assign_label_linenumbers(label_env, linenumber_env)

            in_env = 0
            text_env = ""
            label_env = ""

        # Closeout proof
        if end_of_proof(line):
            in_proof = 0
            # We pick up only the first proof if there are multiple proofs
            if label_proof:
                if not text_proof:
                    exit(1)
                proof_texts[label_proof] = text_proof
            text_proof = ""
            label_proof = ""

        # Closeout item
        if line.find('\\end{enumerate}') == 0 or line.find('\\end{itemize}') == 0 or line.find('\\end{list}') == 0:
            if in_item and label_item:
                assign_label_text(label_item, text_item)
                linenumber_item[1] = line_nr
                assign_label_linenumbers(label_item, linenumber_item)

                label_item = ""
            in_item = 0
            text_item = ""
            label_item = ""

        # Closeout section/subsection/subsubsection
        if line.find('\\input{chapters}') == 0:
            if in_section:
                assign_label_text(label_section, text_section)
                linenumber_section[1] = line_nr - 1
                assign_label_linenumbers(label_section, linenumber_section)

                in_section = 0
                text_section = ""
                label_section = ""
            if in_subsection:
                assign_label_text(label_subsection, text_subsection)
                linenumber_subsection[1] = line_nr - 1
                assign_label_linenumbers(label_subsection, linenumber_subsection)

                in_subsection = 0
                text_subsection = ""
                label_subsection = ""
            if in_subsubsection:
                assign_label_text(label_subsubsection, text_subsubsection)
                linenumber_subsubsection[1] = line_nr - 1
                assign_label_linenumbers(label_subsubsection, linenumber_subsubsection)

                in_subsubsection = 0
                text_subsubsection = ""
                label_subsubsection = ""

        # Closeout equation
        if line.find('\\end{equation}') == 0:
            in_equation = 0
            assign_label_text(label_equation, text_equation)
            linenumber_equation[1] = line_nr
            assign_label_linenumbers(label_equation, linenumber_equation)

            text_equation = ""
            label_equation = ""

        # Closeout reference
        if line.find('\\end{reference}') == 0:
            in_reference = 0
            linenumber_reference[1] = line_nr
            # We pick up only the first reference if there are multiple
            # references
            if label_reference:
                if not text_reference:
                    exit(1)
                # remove \begin and \end
                reference_texts[label_reference] = "\n".join(text_reference.split("\n")[1:-2])
            text_reference = ""
            label_reference = ""

    tex_file.close()


# ZZZZ is a special case
text = 'Tag ZZZZ. If a result has been labeled with tag ZZZZ<br>\n'
text = text + 'this means the result has not been given a stable tag yet.'

# remove all proofs from a chunk of TeX code
def remove_proofs(text):
  result = ''

  in_proof = False
  for line in text.splitlines():
    if beginning_of_proof(line):
      in_proof = True

    if not in_proof:
      result += "\n" + line

    if end_of_proof(line):
      in_proof = False

  return result

# only give the proofs
def extract_proofs(text):
  result = ''

  in_proof = False
  for line in text.splitlines():
    if beginning_of_proof(line):
      in_proof = True

    if in_proof:
      result += "\n" + line

    if end_of_proof(line):
      in_proof = False

  return result

def update_linenumbers(tag, linenumbers):
  # insert the text of the tag in the real table
  try:
    query = 'UPDATE tags SET begin = ?, end = ? WHERE tag = ?'
    connection.execute(query, (linenumbers[0], linenumbers[1], tag))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

def update_text(tag, text):
  # insert the text of the tag in the real table
  try:
    query = 'UPDATE tags SET value = ? WHERE tag = ?'
    connection.execute(query, (text, tag))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  # insert the text of the tag in the fulltext search table
  try:
    query = 'INSERT INTO tags_search (tag, text, text_without_proofs) VALUES(?, ?, ?)'
    connection.execute(query, (tag, text, remove_proofs(text)))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

# Expects a string
# Returns a list of tuples
# Each tuple (a, b) represents an occurence \cite[a]{b}
def get_cites_from_reference(reference):
  # get list of tuples ('[a]', 'a', 'B') for each \cite[a]{B}
  l = re.findall(r"\cite(\[([^]]*)\])?{([^}]+)}", reference)
  return [ (b,c) for (a,b,c) in l ]

def update_reference(tag, reference):
  # insert the text of the reference in the tags table
  try:
    query = 'UPDATE tags SET reference = ? WHERE tag = ?'
    connection.execute(query, (reference, tag))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  # delete all \cite commands (for this tag) from the citations table
  try:
    query = 'DELETE FROM citations WHERE tag = ?'
    connection.execute(query, (tag,))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  # insert \cite commands in the citations table
  cites = get_cites_from_reference(reference)
  for (text, name) in cites:
    try:
      query = 'INSERT INTO citations (tag, name, text) VALUES (?,?,?)'
      connection.execute(query, (tag, name, text))

    except sqlite3.Error, e:
      print "An error occured:", e.args[0]

def get_text(tag):
  try:
    query = 'SELECT value FROM tags where tag = ?'
    cursor = connection.execute(query, [tag])

    value = cursor.fetchone()[0]
    # if the tag is new the database returns None
    if value == None: value = ''
    return value

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]


def clearSearchTable():
  (connection, cursor) = general.connect()

  try:
    query = 'DELETE FROM tags_search'
    connection.execute(query)

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  general.close(connection)


def importLaTeX():
  global connection
  (connection, cursor) = general.connect()

  n = 0
  while n < len(tags):
    tag = tags[n][0]
    label = tags[n][1]
  
    text = ''
  
    if label in label_linenumbers.keys():
      update_linenumbers(tag, label_linenumbers[label])
  
    if label in label_texts:
      text = text + label_texts[label]
  
      if label in proof_texts:
        text = text + '\n' + proof_texts[label]

    # if text has changed and current text isn't empty (i.e. not a new tag)
    if get_text(tag) != text and get_text(tag) != '':
      print "The text of tag", tag, "has changed",
      if label in proof_texts and extract_proofs(get_text(tag)) != extract_proofs(text):
        print "as well as its proof"
      else:
        print ""
        
    # update anyway to fill tags_search which is emptied every time
    update_text(tag, text)

    # if there is a reference, update it
    if label in reference_texts:
      update_reference(tag, reference_texts[label])
  
    n = n + 1

  general.close(connection)
