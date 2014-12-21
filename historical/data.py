import cPickle as pickle

import config

def load_back(commit):
  path = config.historyData + '/' + commit
  fd = open(path, 'rb')
  History = pickle.load(fd)
  fd.close()
  return History


# process a tag determining all the required information for the database
def process_tag(history):
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
      print '  Introduced tag ' + env.tag
      tag = env.tag

      change_type += 'tag '

    # changed the name of the label (or created the tag)
    if env.label != label:
      if label == '':
        print '  Introduced label "' + env.label + '"'
        change_type += 'labelintro '
      else:
        print '  Changed label from "' + label + '" to "' + env.label + '"'
        change_type += 'labelchange '

      label = env.label

    # moved from one file to another (or created the statement)
    if env.name != name:
      if name == '':
        print '  Created the text in "' + env.name + '"'
        change_type += 'creation '
      else:
        print '  Moved files from "' + name + '" to "' + env.name + '"'
        change_type += 'move '

      name = env.name

    # change in the text of the statement (or created the statement)
    if env.text != text:
      print '  Change in text'
      if text != '':
        change_type += 'change '

      text = env.text

    # change in the text of the proof
    if hasattr(env, 'proof'):
      if proof != '':
        change_type += 'proofchange'

      if env.proof != proof:
        proof = env.proof

    # nothing has happened: it must be a move
    if change_type == "":
      print '  Moved inside the file from ' + str(env.b) + '--' + str(env.e)
      lines[0] = env.b
      lines[1] = env.e
      change_type += 'move '


    # print change_type
    if change_type == '':
      print 'This should not happen'

    print ''


def importHistory():
  # TODO this must be dynamic somehow
  history = load_back('5b422bc40419ce8e1c682591edb8d17eea4e1c8f')

  # process commits
  for commit in history.commits:
    print commit # TODO at the moment we don't have the commit log and time available

  for tag in history.env_histories:
    # there must be a tag, otherwise it is not accessible on the website (intermediate commits can have "tag-less tags")
    if tag.env.tag != "":
      process_tag(tag)
