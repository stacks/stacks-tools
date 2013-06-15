import graphs.generate


print "Generating the force-directed graphs"
graphs.generate.generateForceDirectedGraphs()

print "Generating the cluster graphs"
graphs.generate.generateClusterGraphs()

print "Generating the collapsible graphs"
graphs.generate.generateCollapsibleGraphs()

#graphs.generate.scatter()
print "\nClearing the dependencies table"
graphs.generate.clearDependencies()
print "Inserting dependencies"
graphs.generate.insertDependencies()

print "\nCreating various graph related statistics"
graphs.generate.updateCounts()
