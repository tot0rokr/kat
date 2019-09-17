"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io       

cparser.py

tokens: Result of lexical analysis about "*.c" c code
return: constructed tags

"""


from kat.lib.tag import Tag
from kat.lib.file import File

def parse(tokens, fileName=None):
    scope = ["base"]
    state = ["space"]
    tag = Tag()
    tags = []

    path = File(fileName)

    while len(tokens) > 0:
        token = tokens.pop(0)
        tokenType = token[3]
        if state[-1] == "start":
            if tokenType == "T_NEWLINE":
                continue
            elif tokenType == "T_COMMENT_SINGL_LINE":
                state.append("comment_single") 
                continue
            elif tokenType == "T_COMMENT_MULTI_LINE_OPEN":
                state.append("comment_open")
                continue
            elif topenType == "T_PREPROCESS":
                


        elif state[-1] == "comment_single":
            if tokenType == "T_NEWLINE":
                state.pop()
                continue
            else:
                continue
        
        elif state[-1] == "comment_open":
            if tokenType == "T_COMMENT_MULTI_LINE_CLOSE":
                state.pop()
                continue
            else:
                continue

        



        print("state : {}".format(state))
        print(token)
        print(tokens[0])
        raise AssertionError("CsparserSyntaxError")

    return tags


