"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io       

ppparser.py
    preprocess parser

tokens: Result of lexical analysis about preprocesses in "*.c" c code
return: constructed tags

"""


from kat.lib.tag        import Tag
from kat.lib.file       import File
from kat.lib.token      import Token
from kat.lib.scope      import Scope
import re


def parse(tokens, path):
    scope = []
    stack = ["^"]
    tags = []
    includeFiles = []                   # included libraries
                                        # they'll be mapped by pptracer after
                                        # returning this function

    base = path.scope
    scope.append(base)

    tokens.append(Token("$"))      # This is only used by last chunk

    def shift(from, to, symbol, state):
        to.append(from.pop(0))
        
    def pop(list):
        list.pop(0)

    
    #  while len(tokens) > 0:
    while true:
        if stack[-1] == "space":
            if tokens[0].kind == "T_NEWLINE":
                tokens.pop(0)

            elif tokens[0].kind == "T_COMMENT_SINGL_LINE":
                tokens.pop(0)
                stack.append("comment_single") 

            elif tokens[0].kind == "T_COMMENT_MULTI_LINE_OPEN":
                tokens.pop(0)
                stack.append("comment_open")

            elif tokens[0].kind == "T_INCLUDE_STD_H":
                #  includeFilePath = re.compile(r"<(.*)>").search(token.substance).group(1)
                #  includeFiles.append(includeFilePath)
                includeFiles.append(tokens.pop(0).substance)

            elif tokens[0].kind == "T_INCLUDE_USR_H":
                print(path() + "Is it exist? " + tokens.pop(0).substance)

            elif tokens[0].kind == "T_PREPROCESS_DEFINE":
                tokens.pop(0)
                stack.append("define")

            elif tokens[0].kind == "T_PREPROCESS_DEFINEFUNC":
                tokens.pop(0)
                stack.append("definefunc")

            else:
                break
            continue    

        elif stack[-1] == "comment_single":
            if tokens[0].kind == "T_NEWLINE":
                tokens.pop(0)
                stack.pop()
            else:
                tokens.pop(0)
            continue
        
        elif stack[-1] == "comment_open":
            if tokens[0].kind == "T_COMMENT_MULTI_LINE_CLOSE":
                tokens.pop(0)
                stack.pop()
            else:
                tokens.pop(0)
            continue
                    

        elif stack[-1] == "define":
            if tokens[0].kind == "T_IDENTIFIER":
                stack.append(tokens.pop(0))
                stack.append("define_id")
            else:
                break
            continue

        elif stack[-1] == "definefunc":
            if 








        #  token = tokens.pop(0)
        #  if tokens[0].kind == "T_NEWLINE":
            #  if symbol[-1] == "space":
                #  continue
            #  if symbol[-1] == "comment_single":
                #  symbol.pop()
                #  continue

        #  if tokens[0].kind == "T_COMMENT_SINGL_LINE":
            #  if (symbol[-1] == "comment_single"
                    #  or symbol[-1] == "comment_open"
                    #  or symbol[-1] == "string"):
                #  continue
            #  else:
                #  symbol.append("comment_single")
                #  continue

        #  if tokens[0].kind == "T_COMMENT_MULTI_LINE_OPEN":
            #  if (
    if token is not "T_LAST":
        print("state : {}".format(state))
        print(token)
        print(tokens[0])
        raise AssertionError("CsparserSyntaxError")

    return (tags, includeFiles)


