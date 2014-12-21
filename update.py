import bibliography.update, historical.data, statistics.commits, statistics.counts, tags.tags, tags.tex, tags.titles

# see documentation in historical/classes.py for the explanation...
# there is also a name clash which I want to avoid by naming the module historical
from historical.classes import env_with_proof, env_without_proof, env_history, history

print "Taking care of the bootstrap"
tags.tags.importBootstrap()
print "Importing tags"
tags.tags.importTags()
print "Cleaning removed tags"
tags.tags.checkTags()

print "\nClearing search table"
tags.tex.clearSearchTable()
print "\nImporting LaTeX code"
tags.tex.importLaTeX()

print "\nUpdating the line counts"
statistics.counts.updateLineCounts()
print "Updating the page counts"
statistics.counts.updatePageCounts()

print "\nUpdating commit information"
statistics.commits.updateCommits()

print "\nClearing bibliography"
bibliography.update.clearBibliography()
print "Importing bibliography"
bibliography.update.importBibliography()

print "\nImporting titles"
tags.titles.importTitles()

print "\nImporting history"
historical.data.importHistory()
