import itertools, sqlite3, string, subprocess
# import config TODO fix configuration

# execute a command in the correct Pythonesque way
def execute(command):
    process = subprocess.Popen(command, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, close_fds = True, cwd = "../stacks-project") # TODO configuration
    return (process.stdout.read(), process.stderr.read())

# find the label corresponding to a tag (even inactive tags)
def getLabel(tag):
  f = open("../stacks-project/tags/tags", "r") # TODO configuration

  for line in f:
    if line[0:4] == tag: return line.split(",")[1][0:-1]
    if line[0:5] == "#" + tag: return line.split(",")[1][0:-1]

  return ""

def getLineNumber(tag):
  f = open("../stacks-project/tags/tags", "r") # TODO configuration

  for (number, line) in enumerate(f, 1):
    if line[0:4] == tag: return number
    if line[0:5] == "#" + tag: return number

  return 0

def getOriginalLineNumber(lineNumber, start = "HEAD"):
  # assuming it is always on the first line
  command = "git blame -L" + str(lineNumber) + ",+1 " + str(start) + " tags/tags -n -p"
  (output, error) = execute(command)

  # we get an error, which means that the line didn't exist, ergo it was added in this commit
  if error != "":
    return (lineNumber, start)

  # these are on the first line
  previousNumber = output.split("\n")[0].split(" ")[1]
  # this one is prefixed previous
  previousCommit = filter(lambda s: s[0:8] == "previous", output.split("\n"))
  # we've gone all the way to the original tags file
  if previousCommit == []:
    return (previousNumber, output.split("\n")[0].split(" ")[0].strip())
  else:
    return getOriginalLineNumber(previousNumber, previousCommit[0].split(" ")[1].strip())

def getCreationDate(tag):
  lineNumber = getLineNumber(tag)
  (originalLineNumber, originalCommit) = getOriginalLineNumber(lineNumber)

  command = "git show -s --format=\"%ct\" " + str(originalCommit)
  (output, error) = execute(command)

  return (output.strip(), originalCommit)

def getTags():
  try:
    query = "SELECT tag FROM tags ORDER BY tag"
    cursor = connection.execute(query)

    tags = cursor.fetchall()
    return [tag[0] for tag in tags] # get first (and only) column

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

def getModificationDate(tag):
  lineNumber = getLineNumber(tag)

  command = "git blame -L" + str(lineNumber) + ",+1 tags/tags -p"
  (output, error) = execute(command)
  return (filter(lambda s: s[0:11] == "author-time", output.split("\n"))[0].split(" ")[1], output.split("\n")[0].split(" ")[0])

def tagExists(tag):
  return getLineNumber(tag) != 0

# Test the code (future changes might not be reflected here)
"""
def information(tag):
  if not tagExists(tag):
    # print "the tag " + str(tag) + " does not exist"
    return

  lineNumber = getLineNumber(tag)
  print "the tag " + str(tag) + " currently has line number: " + str(lineNumber)
  label = getLabel(tag)
  print "its label is: " + label

  modificationDate = getModificationDate(lineNumber)
  print "it was last modified on: " + modificationDate
  creationDate = getCreationDate(tag)
  print "it was created on: " + creationDate

for tag in itertools.product(string.digits + string.ascii_uppercase, repeat = 4):
    information(''.join(tag))
"""

def updateCommitInformation(tag):
  # TODO check for existence of a tag first, if it doesn't exist this is an error

  print "Updating " + tag

  (creationDate, creationCommit) = getCreationDate(tag)
  (modificationDate, modificationCommit) = getModificationDate(tag)

  try:
    query = "UPDATE tags SET creation_date = ?, creation_commit = ?, modification_date = ?, modification_commit = ? WHERE tag = ?"
    connection.execute(query, [creationDate, creationCommit, modificationDate, modificationCommit, tag])

    # TODO move this
    connection.commit()

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

connection = sqlite3.connect("../stacks-website/database/stacks.sqlite")

# we use the tags present in the database
tags = getTags()
map(updateCommitInformation, tags)

connection.commit()
connection.close()
