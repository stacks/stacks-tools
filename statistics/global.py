import sqlite3
# TODO find good package approach in Python (is there one?!)
import subprocess

# execute a command in the correct Pythonesque way
# TODO move this to general.py in root
def execute(command):
    process = subprocess.Popen(command, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, close_fds = True, cwd = "../../stacks-project") # TODO configuration
    return (process.stdout.read(), process.stderr.read())

def keyExists(key):
  try:
    query = "SELECT COUNT(*) FROM statistics WHERE key = ?"
    cursor = connection.execute(query, [key])

    return cursor.fetchone()[0] > 0

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]
 

def update(key, value):
  try:
    if keyExists(key):
      query = 'UPDATE statistics SET value = ? WHERE key = ?'
      connection.execute(query, [value, key])
    else:
      query = 'INSERT INTO statistics (key, value) VALUES (?, ?)'
      connection.execute(query, [key, value])

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]


def updateLineCounts():
  command = "wc -l *.tex"
  (output, error) = execute(command)

  for line in filter(None, output.split("\n")):
    (linecount, filename) = line.split()
    update("linecount " + filename, linecount)


# TODO fix config
connection = sqlite3.connect("../../stacks-website/database/stacks.sqlite")

updateLineCounts()

connection.commit()
connection.close()
