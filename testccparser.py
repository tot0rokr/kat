from kat.lib.tag import Tag
from kat.tracer import ccscanner as ccs
from kat.tracer import ccparser as ccp

f = open(".config", "r")
data = f.read()
f.close()



for it in ccp.parse(ccs.scan(data)):
    print(it)

    # print("Name: {2} / Type: {3} / LineNum: {1} / Line: {0}".format(it[0] + it[1] + it[2] + it[3]))

