import config

# this is a silly name for the file, but the obvious import.py is forbidden

def addMacro(name, value, cursor):
  try:
    query = 'INSERT INTO macros (name, value) VALUES (?, ?)'
    cursor.execute(query, [name, value])

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

def addMacros(cursor):
  f = open(config.websiteProject + "/preamble.tex", "r")

  # Convention in the Stacks project
  # A command always starts with a \ and is follows by a sequence
  # of characters out of the following set of characters:
  S = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

  for line in f:
    if line[0:5] == '\\def\\':
      line = line.rstrip()
      if not line[-1] == '}':
        print "Misformed definition in preamble.tex: " + line
	exit(1)
      n = 5
      while line[n] in S: n = n + 1
      if not line[n] == '{':
        print "Misformed definition in preamble.tex: " + line
        exit(1)
      name = line[4:n]
      value = line[n + 1:-1]
  
      addMacro(name, value, cursor)

def clearMacros(cursor):
  try:
    query = 'DELETE FROM macros'
    cursor.execute(query)

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

