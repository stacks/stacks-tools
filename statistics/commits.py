import itertools, sqlite3, string

import config, general

# find the label corresponding to a tag (even inactive tags)
def getLabel(tag):
  f = open(config.websiteProject + "/tags/tags", "r")

  for line in f:
    if line[0:4] == tag: return line.split(",")[1][0:-1]
    if line[0:5] == "#" + tag: return line.split(",")[1][0:-1]

  return ""


def getLineNumber(tag):
  f = open(config.websiteProject + "/tags/tags", "r")

  for (number, line) in enumerate(f, 1):
    if line[0:4] == tag: return number
    if line[0:5] == "#" + tag: return number

  return 0


def getOriginalLineNumber(lineNumber, start = "HEAD"):
  # assuming it is always on the first line
  command = "git blame -L" + str(lineNumber) + ",+1 " + str(start) + " tags/tags -n -p"
  (output, error) = general.execute(command)

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
  (output, error) = general.execute(command)

  return (output.strip(), originalCommit)


def getTags(cursor):
  try:
    query = "SELECT tag FROM tags ORDER BY tag"
    result = cursor.execute(query)

    tags = result.fetchall()
    return [tag[0] for tag in tags] # get first (and only) column

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]


def getModificationDate(tag):
  lineNumber = getLineNumber(tag)

  command = "git blame -L" + str(lineNumber) + ",+1 tags/tags -p"
  (output, error) = general.execute(command)
  return (filter(lambda s: s[0:11] == "author-time", output.split("\n"))[0].split(" ")[1], output.split("\n")[0].split(" ")[0])


def tagExists(tag):
  return getLineNumber(tag) != 0


def updateCommitInformation(tag, cursor):
  # TODO check for existence of a tag first, if it doesn't exist this is an error

  print "Updating " + tag

  (creationDate, creationCommit) = getCreationDate(tag)
  (modificationDate, modificationCommit) = getModificationDate(tag)

  try:
    query = "UPDATE tags SET creation_date = ?, creation_commit = ?, modification_date = ?, modification_commit = ? WHERE tag = ?"
    cursor.execute(query, [creationDate, creationCommit, modificationDate, modificationCommit, tag])

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]


def updateCommits():
  (connection, cursor) = general.connect()

  tags = getTags(cursor)
  for tag in tags:
    updateCommitInformation(tag, cursor)

  general.close(connection)
