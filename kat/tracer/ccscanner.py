"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io

curconfigscanner.py

return: Token(kind, substance, line, line_nr)
kind: a semantic type of unit
substance: useful string matched
line: a line of token
line_nr: a number of line
unit: a name of minimum unit of line
token: a semantic type of unit processed by scanner

"""

import re
from kat.tracer.cc_tokenlib import *
from kat.lib.token  import *


def scan(rawdata):
    tokens = []
    line_nr = 0

    tokens.append(CurConfigToken(token_kind['T_FIRST']))
    for line in rawdata.split("\n"):
        line_nr = line_nr + 1
        text = line
        while len(text) > 0:
            success = False
            for it in range(len(regex)):
                matched_string = regex[it].match(text)
                if matched_string is not None:
                    if it == 0 or it == token_kind['T_COMMENT'] or it == token_kind['T_OPERATOR']:
                        text = text[matched_string.end():]
                        success = True
                        break
                    substance = matched_string.group()
                    kind = it
                    text = text[matched_string.end():]
                    token = CurConfigToken(kind=kind, line_nr=line_nr, substance=substance)
                    tokens.append(token)
                    success = True
                    break
            if success is True:
                continue

            print("it : ", it)
            if substance is not None:
                print("substance : ", substance)
            print("line_nr : ", line_nr)
            raise AssertionError("ccscanner.py")

    #  return tokens
    return tokens


