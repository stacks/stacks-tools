import bibliography.update, statistics.commits, statistics.counts, tags.tags

print "Updating the line counts"
statistics.counts.updateLineCounts()
print "Updating the page counts"
statistics.counts.updatePageCounts()

print "\nUpdating commit information"
statistics.commits.updateCommits()

print 'Clearing bibliography'
bibliography.update.clearBibliography()
print 'Importing bibliography'
bibliography.update.importBibliography()

print 'Taking care of the bootstrap'
tags.tags.importBootstrap()
print 'Importing tags'
tags.tags.importTags()
print 'Cleaning removed tags'
tags.tags.checkTags()
