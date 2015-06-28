import config
import historical.data
import os.path

# see documentation in historical/classes.py for the explanation...
# there is also a name clash which I want to avoid by naming the module historical
from historical.classes import env_with_proof, env_without_proof, env_history, history

commit = raw_input("Which commit do you want to load?\n")

if not os.path.isfile(config.historyData + "/" + commit):
  print "ERROR: This commit does not exist in " + config.historyData
else:
  print "\nClearing history"
  historical.data.clearHistory()
  print "\nImporting history"
  historical.data.importHistory(commit)
