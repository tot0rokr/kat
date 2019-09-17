from kat.lib.tag import Tag
from kat.tracer import curconfigscanner as ccs

f = open(".config", "r")
data = f.read()
f.close()


for it in ccs.scan(data):
    print(it)

    # print("Name: {2} / Type: {3} / LineNum: {1} / Line: {0}".format(it[0] + it[1] + it[2] + it[3]))

