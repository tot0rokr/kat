from kat.tracer import ppscanner as pps
from kat.tracer import ppparser as ppp
from kat.lib.file import File
from kat.lib.scope import Scope

testfile = "test9.h"
f = open(testfile, "r")
data = f.read()
f.close()

debug = open("testppp.debug", "w")

tokens = pps.scan(data, testfile)

path = File(testfile, "./")
path.scope = Scope(path, None, 0, 0)

tags, files, scopes = ppp.parse(tokens, path)

debug.write("------defined tags-----\n")
for it in tags:
    debug.write(str(it))
    debug.write("\n")

debug.write("------include files-----\n")
for it in files:
    debug.write(str(it))
    debug.write("\n")

debug.write("------included scope-----\n")
for it in scopes:
    debug.write(str(it))
    debug.write("\n")


debug.close()
