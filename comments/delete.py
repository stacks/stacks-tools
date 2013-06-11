import sqlite3, string, sys

import config, general

# check whether a comment exists in the database
def commentExists(ID):
  try:
    query = 'SELECT COUNT(*) FROM comments WHERE id = ?'
    cursor = connection.execute(query, [ID])

    return cursor.fetchone()[0] == 1

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  return False

# get a comment from the database
def getComment(ID):
  assert commentExists(ID)

  try:
    query = 'SELECT id, author, date, tag FROM comments WHERE id = ?'
    cursor = connection.execute(query, [ID])

    return cursor.fetchone()

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

# delete a comment from the database
def deleteComment(ID):
  assert commentExists(ID)

  try:
    query = 'DELETE FROM comments WHERE id = ?'
    connection.execute(query, [ID])

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]


if not len(sys.argv) == 2:
  print 'You must supply one argument, namely the id of the comment you wish to remove'
  raise Exception('Wrong number of arguments')

ID = int(sys.argv[1])

print 'Trying to remove the comment with id', int(ID)

(connection, cursor) = general.connect()

if not commentExists(ID):
  print 'There is no such comment in the database'
else:
  comment = getComment(ID)
  choice = raw_input('Are you sure you wish to remove this comment by ' + comment[1] + ' on tag ' + comment[3] + '? (Y/N): ')
  if string.upper(choice) == 'Y':
    deleteComment(ID)
    print 'Comment removed!'

connection.commit()
connection.close()
