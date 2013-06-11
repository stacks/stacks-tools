# This script creates an empty database as used by stacks-website
# After creation it should be placed in a directory with the correct chmod

import os.path, sqlite3, sys

def execute(filename):
  query = open("database/" + filename, "r").read()
  cursor = connection.cursor()
  cursor.execute(query)

tables = ["bibliography_items.sql", "bibliography_values.sql", "comments.sql", "macros.sql", "sections.sql", "statistics.sql", "tags.sql", "tags_search.sql"]
indices = "indices.sql"

if os.path.isfile("stacks.sqlite"):
  print "The file stacks.sqlite already exists in this folder, aborting"
  sys.exit()

print "Creating the database in stacks.sqlite"

connection = sqlite3.connect("stacks.sqlite")

map(execute, tables)
execute(indices)

connection.commit()
connection.close()

print "The database has been created"
