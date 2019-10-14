"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io

ppscaner.py
    Preprocess Scanner

return: Token(kind, substance, line_nr, line)
line: a line of token
line_nr: a number of line
substance: a name of minimum unit of line
kind: a semantic type of unit processed by scanner


tokens:
    T_NEWLINE
    T_COMMENT_SINGL_LINE
    T_COMMENT_MULTI_LINE_OPEN
    T_COMMENT_MULTI_LINE_CLOSE
    T_PREPROCESS
    T_DATATYPE
    T_KEYWORD
    T_QUOTES_DOUBLE
    T_QUOTES_SINGLE
    T_VARIABLE_ARGUMENTS
    T_COMMA
    T_IDENTIFIER
    T_PARENTHESIS_OPEN
    T_PARENTHESIS_CLOSE
    T_SEMICOLON
    T_BACKSLASH

"""

from kat.lib.token    import Token
import re
from kat.tracer.tokenlib import *

#  regexList = [
    #  (space, None),
    #  (commentSingleLine, "T_COMMENT_SINGL_LINE"),
    #  (commentMultiLineOpen, "T_COMMENT_MULTI_LINE_OPEN"),
    #  (commentMultiLineClose, "T_COMMENT_MULTI_LINE_CLOSE"),
    #  (preprocess, "T_PREPROCESS"),
    #  (datatype, "T_DATATYPE"),
    #  (keyword, "T_KEYWORD"),
    #  (quotesDouble, "T_STRING"),
    #  (quotesSingle, "T_CHARACTOR"),
    #  (floating, "T_FLOATING"),
    #  (integer, "T_INTEGER"),
    #  (operator, "T_OPERATOR"),
    #  (comma, "T_COMMA"),
    #  (identifier, "T_IDENTIFIER"),
    #  (parenthesisOpen, "T_PARENTHESIS_OPEN"),
    #  (parenthesisClose, "T_PARENTHESIS_CLOSE"),
    #  (braceOpen, "T_BRACE_OPEN"),
    #  (braceClose, "T_BRACE_CLOSE"),
    #  (bracketOpen, "T_BRACKET_OPEN"),
    #  (bracketClose, "T_BRACKET_CLOSE"),
    #  (semicolon, "T_SEMICOLON"),
    #  (backslash, "T_BACKSLASH"),
    #  (etcCharators, "T_ETC")
#  ]



def scan(rawdata):
    tokens = []
    debug = ""
    line_cnt = 0
    line_nr = 0
    tmp = 0
    token_nr = 0

    tokens.append(Token(token_kind['T_FIRST']))

    preprocesses = []

    lines = ""
    for line in rawdata.split('\n'):
        line_cnt += 1           # line count
        if re.compile(r"\\[ \t]*$").search(line) is not None:
            tmp += 1            # for counting two or more of lines
            lines += line + "\n" # add newline escape key because of split('\n')
            continue
        else:
            line_nr = line_cnt - tmp    # line number of preprocess
            tmp = 0
            lines += line

        lines += "\n"
        matchedString = preprocess.match(lines) # make matchedString as preprocess
                                                # about lines
        lines = ""                              # re-initialize 0
        if matchedString is None:               # if it is not preprocess
                                                # go to next line
            continue

        key = [matchedString.group(2), matchedString.group(3)]
        if key[0] == "include":
            matchedString = re.compile('[ \t]?([<"])(.*)[>"]').search(key[1])

            if matchedString.group(1) == "<":
                token = Token(line=lines, line_nr=line_nr
                        , substance=matchedString.group(2), kind=token_kind["T_INCLUDE_STD_H"])
                tokens.append(token)
            elif matchedString.group(1) == '"':
                token = Token(line=lines, line_nr=line_nr
                        , substance=matchedString.group(2), kind=token_kind["T_INCLUDE_USR_H"])
                tokens.append(token)
            else:
                raise AssertionError("ppscanner: include")
            token = Token(token_kind["T_NEWLINE"])
            tokens.append(token)

            continue
        elif key[0] == "if":
            pass
            # [^:A-Za-z0-9_ \t\(\)&\|\*\!(/*)(*/)><=\.\-,]
        elif key[0] == "ifdef":
            pass
        elif key[0] == "ifndef":
            pass
        elif key[0] == "else":
            token = Token(line=lines, line_nr=line_nr
                    , substance=preprocess_kind[key[0]], kind=token_kind["T_PREPROCESS"])
                    #  , substance=None, kind=token_kind["T_PREPROCESS_"+key[0].upper()])
            tokens.append(token)
            token = Token(token_kind["T_NEWLINE"])
            tokens.append(token)
            continue
        elif key[0] == "elif":
            pass
        elif key[0] == "endif":
            token = Token(line=line, line_nr=line_nr
                    , substance=preprocess_kind[key[0]], kind=token_kind["T_PREPROCESS"])
                    #  , substance=None, kind=token_kind["T_PREPROCESS_"+key[0].upper()])
            tokens.append(token)
            token = Token(token_kind["T_NEWLINE"])
            tokens.append(token)
            continue
        elif key[0] == "define":
            key[0] = "macro"
            matchedString = re.compile('define[ \t]+[A-Za-z_][A-Za-z_0-9]*\(').match(key[1])
            if matchedString is not None:
                key[0] = "macrofunc"

        elif key[0] == "error":
            pass
        elif key[0] == "undef":
            pass
        elif key[0] == "pragma":
            pass
        elif key[0] == "warning":
            pass
        elif key[0] == "line":
            pass


        token = Token(line=lines, line_nr=line_nr
                , substance=preprocess_kind[key[0]], kind=token_kind["T_PREPROCESS"])
                #  , substance=None, kind=token_kind["T_PREPROCESS_"+key[0].upper()])
        tokens.append(token)

        text = key[1]
        while len(text) > 0:
            success = False
            for outer_it in range(len(regex)):
                matched_string = regex[outer_it].match(text)
                if matched_string is not None:
                    if outer_it == 0:
                        text = text[matched_string.end():]
                        success = True
                        break
                    substance = matched_string.group()
                    kind = outer_it
                    if outer_it == token_kind['T_IDENTIFIER']:
                        for inner_it in range(token_kind['T_IDENTIFIER'] + 1,
                                token_kind['T_SIZEOF'] + 1):
                            inner_matched_string = regex[inner_it].match(text)
                            if inner_matched_string is not None \
                                    and inner_matched_string.group() == matched_string.group():
                                kind = inner_it
                                break
                    text = text[matched_string.end():]
                    token = Token(kind=kind, line_nr=line_nr, substance=substance)
                    tokens.append(token)
                    success = True
                    break
            if success is True:
                continue

            print("outer_it : ", outer_it)
            print("inner_it : ", inner_it)
            if substance is not None:
                print("substance : ", substance)
            print("line_nr : ", line_nr)
            raise AssertionError("ppascanner.py")

    return tokens               # scanner test

