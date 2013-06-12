import sqlite3

import general, config

def clearBibliography():
  (connection, cursor) = general.connect()

  try:
    query = 'DELETE FROM bibliography_items'
    cursor.execute(query)

    query = 'DELETE FROM bibliography_values'
    cursor.execute(query)

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  general.close(connection)

def insertItem(item, cursor):
  try:
    query = 'INSERT INTO bibliography_items (name, type) VALUES (?, ?)'
    cursor.execute(query, (item[0][1], item[0][0]))

    for (key, value) in item[1].iteritems():
      query = 'INSERT INTO bibliography_values (name, key, value) VALUES (?, ?, ?)'
      cursor.execute(query, (item[0][1], key, value))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

def importBibliography():
  (connection, cursor) = general.connect()
  f = open(config.websiteProject + "/my.bib")

  items = []
  in_item = 0
  line_nr = 0

  for line in f:
    line_nr = line_nr + 1
    # beginning of a new item
    if line[0] == '@':

      if in_item == 1:
        print "On line:", line_nr, "of my.bib:"
	print line
        print "Nested items. Exiting."
	exit(1)

      # clear previous item
      item = [[], {}]

      bib_type = line.partition('{')[0].strip('@').lower()
      name = line.partition('{')[2].strip().strip(',')

      item[0] = (bib_type, name)

      in_item = 1

      continue
  
    # end of an item
    if line[0] == '}':

      if in_item == 0:
        print "On line:", line_nr, "of my.bib:"
        print line
	print "Nested items. Exiting."
	exit(1)

      # add a *copy* to the list of items
      items.append(list(item))

      in_item = 0

      continue

    # can ignore current line if not in an item
    if in_item == 0:

      continue
 
    # ignore comments
    if line[0] == '%' or line[0:2] == '//':

      continue

    # Get key value pair from the line if it contains = sign
    if '=' in line:
      key = line.partition('=')[0].strip().lower()
      value = line.partition('=')[2].strip().strip(',')[1:-1]
      item[1][key] = value

      # Check for correctness
      if not (line.strip()[-2:] == '},' or line.strip()[-2:] == '",' or line.strip()[-1] == '}' or line.strip()[-1:] == '"'):
        print "Warning: run over on line:", line_nr, "in my.bib:"
        print line
        print "Should not happen: each key = value pair should be on a line!"
	print "Exiting"
	exit(1)

  for item in items:
    insertItem(item, cursor)

  general.close(connection)

