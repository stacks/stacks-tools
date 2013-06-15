import sqlite3

import config, general
from functions import *

connection = 0

# check whether a given title exists in the database
# TODO: this should also check whether the title occurs
# in the correct chapter
def title_exists(title):
  try:
    query = 'SELECT COUNT(*) FROM sections WHERE title = ?'
    result = connection.execute(query, [title])

    return result.fetchone()[0]

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  return False

def title_number_exists(number):
  try:
    query = 'SELECT COUNT(*) FROM sections WHERE number = ?'
    result = connection.execute(query, [number])

    return result.fetchone()[0] == 1

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  return False

def insert_title(number, title, filename):
  try:
    if title_number_exists(number):
      query = 'UPDATE sections SET title = ?, filename = ? WHERE number = ?'
      connection.execute(query, (title, filename, number))
    else:
      query = 'INSERT INTO sections (number, title, filename) VALUES (?, ?, ?)'
      connection.execute(query, (number, title, filename))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

def importTitles():
  global connection
  (connection, cursor) = general.connect()

  print 'Creating a database version of the table of contents'
  print 'Parsing the files, linking chapters to file names'
  titles = get_titles(config.websiteProject + "/tags/tmp/")
  print 'Parsing the big table of contents'
  sections = parse_book_toc(config.websiteProject + "/tags/tmp/book.toc")

  # print out new or changed titles before updating the database
  for section in sections:
    if title_exists(section[2]) == 0 and not section[2] == 'Bibliography':
      print 'New or changed section \'%s\'' % (section[2])

  print 'Inserting the information into the database'
  for section in sections:
    # the bibliography doesn't correspond to a file, we can safely ignore it
    if section[2] == 'Bibliography':
      continue

    insert_title(section[1], section[2], find_file_for_section(titles, sections, section[1]))

  general.close(connection)
