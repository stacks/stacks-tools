import cPickle as pickle
import sqlite3

import general, config

def clearHistory():
  (connection, cursor) = general.connect()

  try:
    query = 'DELETE FROM commits' 
    cursor.execute(query)

    query = 'DELETE FROM changes'
    cursor.execute(query)

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  general.close(connection)


def load_back(commit):
  path = config.historyData + '/' + commit
  fd = open(path, 'rb')
  History = pickle.load(fd)
  fd.close()
  return History


def insertCommit(commit, cursor):
  try:
    query = 'INSERT INTO commits (hash) VALUES (?)'
    cursor.execute(query, (commit,))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

def insertChange(change, tag, commit, env, begin, end, cursor):
  try:
    query = 'INSERT INTO changes (type, tag, hash, file, label, begin, end) VALUES (?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(query, (change, tag, commit, env.name, env.label, begin, end))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]


# process a tag determining all the required information for the database
def process_tag(history, cursor):
  print 'Considering ' + history.env.tag

  label = ''
  tag = ''
  name = ''
  text = ''
  proof = ''
  lines = [0, 0]

  for commit, env in zip(history.commits, history.envs):
    print ' Considering ' + commit

    change_type = ''

    # assigned a tag to the statement
    if env.tag != tag:
      insertChange('tag', history.env.tag, commit, env, env.b, env.e, cursor)
      tag = env.tag

      change_type += 'tag '

    # changed the name of the label (or created the tag)
    if env.label != label:
      if label != '':
        insertChange('label', history.env.tag, commit, env, env.b, env.e, cursor)

      label = env.label

      change_type += 'label '

    # moved from one file to another (or created the statement): this is the one we'll treat as the creation
    if env.name != name:
      if name == '':
        insertChange('creation', history.env.tag, commit, env, env.b, env.e, cursor)
      else:
        insertChange('move', history.env.tag, commit, env, env.b, env.e, cursor)

      name = env.name

      change_type += 'filename '

    # change in the text of the statement (or created the statement)
    if env.text != text:
      if text != '':
        insertChange('statement', history.env.tag, commit, env, env.b, env.e, cursor)

      text = env.text

      change_type += 'statement '

    # change in the text of the proof
    if hasattr(env, 'proof'):
      if proof != '':
        insertChange('proof', history.env.tag, commit, env, env.bp, env.ep, cursor)

      if env.proof != proof:
        proof = env.proof

      change_type += 'proof '

    # nothing has happened: it must be a move
    if change_type == '':
      insertChange('move', history.env.tag, commit, env, env.b, env.e, cursor)

      lines[0] = env.b
      lines[1] = env.e

    print ''


def importHistory():
  # TODO this must be dynamic somehow
  history = load_back('5b422bc40419ce8e1c682591edb8d17eea4e1c8f')

  (connection, cursor) = general.connect()

  # process commits
  for commit in history.commits:
    insertCommit(commit, cursor) # TODO at the moment we don't have the commit log and time available

  for tag in history.env_histories:
    # there must be a tag, otherwise it is not accessible on the website (intermediate commits can have "tag-less tags")
    if tag.env.tag != "":
      process_tag(tag, cursor)

  general.close(connection)
