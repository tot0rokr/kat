"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io

curconfigscanner.py

return: tuple(line, line_nr, unit, token)
line: a line of token
line_nr: a number of line
unit: a name of minimum unit of line
token: a semantic type of unit processed by scanner

"""

import re

space = re.compile("[ \t\r\n\v\f]")
identifier = re.compile(r"CONFIG_([a-zA-Z0-9_]*)")
comment = re.compile("#.*")
#  keyword = re.compile(r"""
        #  CONFIG_         # Config prefix
        #  """, re.VERBOSE)
word = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")
string = re.compile("\".*\"")
operator = re.compile("=")
number = re.compile(r"""
        0x[0-9A-Fa-f]+[Uu]?[Ll]{0,2}    # hexadecimal
        | 0[0-7]+[Uu]?[Ll]{0,2}         # octal
        | [1-9][0-9]*[Uu]?[Ll]{0,2}     # decimal
        | 0                             # 0
        """, re.VERBOSE)


def scan(rawdata):
    tokens = []
    line_nr = 0
    for line in rawdata.split("\n"):
        line_nr = line_nr + 1
        text = line
        while len(text) > 0:
            matchedString = space.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                continue

            matchedString = comment.match(text)
            if matchedString is not  None:
                text = text[matchedString.end():]
                continue

            matchedString = identifier.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((line, line_nr, matchedString.group(1), "IDENTIFIER"))
                continue

            matchedString = word.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "WORD"))
                continue
            matchedString = string.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "STRING"))
                continue
            matchedString = number.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "NUMBER"))
                continue
            matchedString = operator.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "OPERATOR"))
                continue

            print(line)
            raise AssertionError("CurconfigscannerNoMatchError")

    #  return tokens
    return tokens

