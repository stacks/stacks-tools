import sqlite3, sys

import config, general
from functions import *

# read all .aux files and generate a dictionary containing all labels and
# their whereabouts
def get_labels_from_source(path):
  # we'll do book.aux first, getting a complete overview of all labels
  aux_files = list_aux_files(path)
  aux_files.remove('book.aux') # do not parse this file again

  print 'Parsing book.aux'
  labels = parse_aux(path + 'book.aux') # generate dictionary with all labels
  
  print 'Parsing the other auxiliary files'
  # now merge every other .aux file against the current dictionary
  for aux_file in aux_files:
    print '  parsing %s' % aux_file
  
    local = parse_aux(path + aux_file)
    for label, information in local.iteritems():
      # we prepend the current filename to get the full label
      full_label = aux_file[0:-4] + '-' + label
  
      if full_label in labels:
        labels[full_label] = [aux_file[0:-4], labels[full_label], local[label]]
      else:
        print 'ERROR: the label \'%s\' was found in %s but not in %s' % (full_label, path + aux_file, path + 'book.aux')

  return labels

def get_label(tag):
  try:
    query = 'SELECT label FROM tags where tag = "' + tag + '"'
    cursor = connection.execute(query)

    return cursor.fetchone()[0]

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]
  

# read all tags from the current tags/tags file
def parse_tags(filename):
  tags_file = open(filename, 'r')

  tags = {}

  for line in tags_file:
    if not line.startswith('#'):
      (tag, label) = line.strip().split(',')
      tags[tag] = label

  tags_file.close()

  return tags

# check whether a tag exists in the database
def tag_exists(tag, cursor):
  count = 0

  try:
    # TODO COUNT(*)
    query = 'SELECT tag FROM tags where tag = "' + tag + '"'
    result = cursor.execute(query)

    if result.fetchone() != None: count = 1

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  return count > 0

def is_active(tag, cursor):
  try:
    query = 'SELECT active FROM tags WHERE tag = ?'
    result = connection.execute(query, [tag])
    return result.fetchone()[0] == 'TRUE'

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  return False
    

def get_tags(cursor):
  try:
    query = 'SELECT tag, active FROM tags'
    result = cursor.execute(query)

    return cursor.fetchall()

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

  return []

def set_inactive(tag, cursor):
  try:
    query = 'UPDATE tags SET active = "FALSE", position = NULL WHERE tag = ?'
    cursor.execute(query, [tag])

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

def set_active(tag):
  try:
    query = 'UPDATE tags SET active = "TRUE" WHERE tag = ?'
    connection.execute(query, [tag])

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]

# insert (or update) a tag
# TODO document the values, or create a Tag class
def insert_tag(tag, value, cursor):
  try:
    if tag_exists(tag, cursor):
      query = 'UPDATE tags SET label = ?, file = ?, chapter_page = ?, book_page = ?, book_id = ?, name = ?, type = ?, position = ? WHERE tag = ?'
      cursor.execute(query, (value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], tag))
    else:
      query = 'INSERT INTO tags (tag, label, file, chapter_page, book_page, book_id, name, type, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
      cursor.execute(query, (tag, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7]))

  except sqlite3.Error, e:
    print "An error occurred:", e.args[0]



def importBootstrap():
  (connection, cursor) = general.connect()

  bootstrap_file = open("tags/bootstrap.txt", 'r')

  for line in bootstrap_file:
    tag, label = line.strip().split(',')
    if not tag_exists(tag, cursor):
      try:
        query = 'INSERT INTO tags (tag, label, active) VALUES (?, ?, "FALSE")'
        cursor.execute(query, (tag, label))

      except sqlite3.Error, e:
        print tag, label
        print "An error occurred:", e.args[0]

    else:
      set_inactive(tag, cursor)

  general.close(connection)

def importTags():
  (connection, cursor) = general.connect()

  print 'Parsing the tags file'
  tags = parse_tags(config.websiteProject + "/tags/tags")

  labels = get_labels_from_source(config.websiteProject + "/tags/tmp/")

  print 'Inserting (or updating) the tags'
  for tag, label in tags.iteritems():
    if label not in labels:
      print 'ERROR, label', label, 'not found in auxiliary files. Have you ran `make tags`?'
      sys.exit()

    if tag_exists(tag, cursor) and get_label(tag, cursor) != label:
      print 'The label for tag %s has changed from \'%s\'to \'%s\'' % (tag, get_label(tag), label)
    if not tag_exists(tag):
      print 'New tag %s with label \'%s\'' % (tag, label)

    info = labels[label]
    insert_tag(tag, (label, info[0], info[2][1], info[1][1], info[1][0], info[1][2], info[2][3], info[1][4]))

  general.close(connection)

# create the tags database from scratch using the current tags/tags file
# loop over all tags and check whether they are still present in the project
def checkTags():
  (connection, cursor) = general.connect()

  print 'Parsing the tags file'
  active_tags = parse_tags(config.websiteProject + "/tags/tags").keys()

  tags = get_tags()

  for tag in tags:
    # check whether the tag is no longer used in the project
    if tag[0] not in active_tags and is_active(tag[0]):
      print '   ', tag[0], 'has become inactive'
      set_inactive(tag[0], cursor)

    # probably not necessary, but check whether a tag is again used in the project
    if tag[1] == 'FALSE' and tag[0] in active_tags:
      print '   ', tag[0], 'has become active again'
      set_active(tag[0])

  general.close(connection)
