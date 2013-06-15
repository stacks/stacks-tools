import sqlite3, subprocess, os

import config

def close(connection):
  connection.commit()

def connect():
  connection = sqlite3.connect(config.database)

  return (connection, connection.cursor())

# execute a command in the correct Pythonesque way
def execute(command):
  process = subprocess.Popen(command, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, close_fds = True, cwd = config.websiteProject)
  return (process.stdout.read(), process.stderr.read())

def href(url):
  return url
