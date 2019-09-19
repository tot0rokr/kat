from kat.tracer import ppscanner as pps
import re

f = open("test3.h", "r")
data = f.read()
f.close()

f1 = open("testpp.debug", "w")

#  f2 = open("test.debug2", "w")

for it in pps.scan(data):
    if it() == "T_NEWLINE":
        #  print("")
        f1.write("\n")
        continue
    if re.compile("T_PREPROCESS|T_INCLUDE").match(it()) is not None:
        #  print("")
        f1.write("\n" + str(it.line_nr) + ": ")
    #  print(it())
    f1.write(str(it()) + " ")

f1.close()
#  f2.close()
    # print("Name: {2} / Type: {3} / LineNum: {1} / Line: {0}".format(it[0] + it[1] + it[2] + it[3]))

print("ppscanner test success")

