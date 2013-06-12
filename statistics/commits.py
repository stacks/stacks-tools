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


def updateCommitInformation(tag, creation, modified, cursor):
  try:
    query = "UPDATE tags SET creation_date = ?, creation_commit = ?, modification_date = ?, modification_commit = ? WHERE tag = ?"
    cursor.execute(query, [creation[0], creation[1], modified[0], modified[1], tag])

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]


def updateCommits():
  (connection, cursor) = general.connect()

  (what, error) = general.execute("git whatchanged --reverse -p tags/tags")
  creation = {}
  modified = {}
  for line in what.split("\n"):
    if line == "":
      continue
    if line.find('commit') == 0:
      commit = line[7:]
      new = 1
      continue
    if line.find('Date') == 0:
      date = line[12:]
      continue
    if line.find('#') >= 0:
      continue
    if line.find('@@') == 0:
      new = 0
      continue
    if new == 0:
      c = line[0]
      if not c == '+':
        continue
      line = line.lstrip(c)
      tag = line.split(',')[0]
      label = line.split(',')[1]
      if tag not in creation:
        creation[tag] = [date, commit]
      modified[tag] = [date, commit]

  tags = getTags(cursor)
  for tag in tags:
    updateCommitInformation(tag, creation[tag], modified[tag], cursor)

  general.close(connection)
