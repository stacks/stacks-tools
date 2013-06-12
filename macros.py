import general, macros.parse

(connection, cursor) = general.connect()

print 'Emptying the table'
macros.parse.clearMacros(cursor)
print 'Importing macros from tex/preamble.tex'
macros.parse.addMacros(cursor)

general.close(connection)
