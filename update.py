import bibliography.update, statistics.commits, statistics.counts

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

