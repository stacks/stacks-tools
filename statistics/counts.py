import sqlite3, subprocess

import config, general

def keyExists(key, cursor):
  try:
    query = "SELECT COUNT(*) FROM statistics WHERE key = ?"
    cursor = cursor.execute(query, [key])

    return cursor.fetchone()[0] > 0

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]
 

def update(key, value, cursor):
  try:
    if keyExists(key, cursor):
      query = 'UPDATE statistics SET value = ? WHERE key = ?'
      cursor.execute(query, [value, key])
    else:
      query = 'INSERT INTO statistics (key, value) VALUES (?, ?)'
      cursor.execute(query, [key, value])

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]


def updateLineCounts():
  (connection, cursor) = general.connect()

  command = "wc -l *.tex"
  (output, error) = general.execute(command)

  for line in filter(None, output.split("\n")):
    (linecount, filename) = line.split()
    update("linecount " + filename, linecount, cursor)

  general.close(connection)


def updatePageCounts():
  (connection, cursor) = general.connect()

  command = "ls tags/tmp/*.log"
  (output, error) = general.execute(command)
  for filename in filter(None, output.split("\n")):
    f = open(config.websiteProject + "/" + filename)
    for line in f:
      if "Output written on " in line:
        update("pagecount " + filename.split("/")[-1].split(".")[0], line.split(" ")[4][1:], cursor)

  general.close(connection)

