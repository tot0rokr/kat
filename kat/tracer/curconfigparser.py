"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io       

curconfigparser.py

tokens: Result of lexical analysis about ".config" file
return: constructed tags

"""

def parse(tokens):
    state = "start"
    tag = {}
    tags = []

    while len(tokens) > 0:
        if state == "start":
            state = "identifier"
            continue
        
        if state == "identifier":
            token = tokens.pop(0)
            if token[3] == "IDENTIFIER":
                tag['name'] = token[2]
                tag['loc'] = {}
                tag['loc']['address'] = {}
                tag['loc']['address']['line'] = token[1]
                tag['loc']['address']['regex'] = "^{}$".format(token[0])
                state = "operator"
                continue

        if state == "operator":
            token = tokens.pop(0)
            if token[3] == "OPERATOR":
                state = "value"
                continue

        if state == "value":
            token = tokens.pop(0)
            if (token[3] == "WORD"
                or token[3] == "STRING"
                or token[3] == "NUMBER"):
                state = "start"
                tag['contents'] = token[2]
                tag['stype'] = "CONFIG"
                tags.append(tag)
                tag = {}
                continue

        print("state : {}".format(state))
        print(token)
        print(tokens[0])
        raise AssertionError("CurconfigsparserSyntaxError")

    return tags


