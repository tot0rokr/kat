from kat.tracer import cscanner as cs

f = open("test.c", "r")
data = f.read()
f.close()

f = open("test.debug", "w")

f2 = open("test.debug2", "w")


for it in cs.scan(data):
    if it[3] == "T_NEWLINE":
        # print("")
        f.write("\n")
        f2.write("\n")
        continue
    # print(it[3], end=' ')
    f.write(it[3] + " ")
    f2.write(str(it[2]) + " ")
    #  print(it[0], end=' ')
    #  print(it[1], end=' ')
    #  print(it[2], end=' ')
    #  print(it[3])

f.close()
f2.close()
    # print("Name: {2} / Type: {3} / LineNum: {1} / Line: {0}".format(it[0] + it[1] + it[2] + it[3]))

print("test success")

