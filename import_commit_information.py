import itertools, string, subprocess

# execute a command in the correct Pythonesque way
def execute(command):
    process = subprocess.Popen(command, shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, close_fds = True)
    return (process.stdout.read(), process.stderr.read())

# find the label corresponding to a tag (even inactive tags)
def getLabel(tag):
    f = open("tags/tags", "r")

    for line in f:
        if line[0:4] == tag: return line.split(",")[1][0:-1]
        if line[0:5] == "#" + tag: return line.split(",")[1][0:-1]

    return ""

def getLineNumber(tag):
    f = open("tags/tags", "r")

    for (number, line) in enumerate(f, 1):
        if line[0:4] == tag: return number
        if line[0:5] == "#" + tag: return number

    return 0

def getOriginalLineNumber(lineNumber, start = "HEAD"):
    # assuming it is always on the first line
    command = "git blame -L" + str(lineNumber) + ",+1 " + str(start) + " tags/tags -n -p"
    (output, error) = execute(command)

    # we get an error, which means that the line didn't exist, ergo it was added in this commit
    if error != "":
        return (lineNumber, start)

    # these are on the first line
    previousNumber = output.split("\n")[0].split(" ")[1]
    # this one is prefixed previous
    previousCommit = filter(lambda s: s[0:8] == "previous", output.split("\n"))
    # we've gone all the way to the original tags file
    if previousCommit == []:
        return (previousNumber, output.split("\n")[0].split(" ")[0])
    else:
        return getOriginalLineNumber(previousNumber, previousCommit[0].split(" ")[1])

def getCreationDate(tag):
    lineNumber = getLineNumber(tag)
    (originalLineNumber, originalCommit) = getOriginalLineNumber(lineNumber)
    print "originally it had line number " + str(originalLineNumber)

    command = "git show -s --format=\"%ct\" " + str(originalCommit)
    (output, error) = execute(command)

    return output

def getModificationDate(lineNumber):
    command = "git blame -L" + str(lineNumber) + ",+1 tags/tags -p"
    (output, error) = execute(command)
    return filter(lambda s: s[0:11] == "author-time", output.split("\n"))[0].split(" ")[1]

def tagExists(tag):
    return getLineNumber(tag) != 0


def information(tag):
    if not tagExists(tag):
        # print "the tag " + str(tag) + " does not exist"
        return

    lineNumber = getLineNumber(tag)
    print "the tag " + str(tag) + " currently has line number: " + str(lineNumber)
    label = getLabel(tag)
    print "its label is: " + label

    modificationDate = getModificationDate(lineNumber)
    print "it was last modified on: " + modificationDate
    creationDate = getCreationDate(tag)
    print "it was created on: " + creationDate

for tag in itertools.product(string.digits + string.ascii_uppercase, repeat = 4):
    information(''.join(tag))
