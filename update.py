import bibliography.update, statistics.commits, statistics.counts, tags.tags, tags.titles

print "Taking care of the bootstrap"
tags.tags.importBootstrap()
print "Importing tags"
tags.tags.importTags()
print "Cleaning removed tags"
tags.tags.checkTags()

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
