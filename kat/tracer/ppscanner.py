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
    T_FLOATING
    T_INTEGER
    T_OPERATOR
    T_COMMA
    T_IDENTIFIER
    T_PARENTHESIS_OPEN
    T_PARENTHESIS_CLOSE
    T_BRACE_OPEN
    T_BRACE_CLOSE
    T_BRACKET_OPEN
    T_BRACKET_CLOSE
    T_SEMICOLON
    T_BACKSLASH
    T_ETC

"""

from kat.lib.token    import Token
import re

space = re.compile("[ \t\r\n\v\f]") # equal with \s
commentSingleLine = re.compile(r"//.*")
commentMultiLineOpen = re.compile(r"/\*")
commentMultiLineClose = re.compile(r"\*/")
#  unsigned = re.compile("unsigned")
preprocess = re.compile(r"""
        ^\#                  # prefix
        (
            (
                [a-z]+              # preprocess word
                #  include | define | ifndef | ifdef | if | elif | else
                #  | endif | error | undef | pragma | warning | line
            ) 
            (
                [ \t]+                  # space
                (
                    /\*.*\*/            # multi line comment
                    | ".*"              # string value
                    | '.'               # charactor value
                    | /                 # divisor operator
                    | [^\\\n"'/]*       # not string and backslash and newline
                )+                      # one or more
                (
                    \\[ \t]*\n          # backslash - several space - newline
                    (
                        /\*.*\*/        # multi line comment
                        | ".*"          # string value
                        | '.'           # charactor value
                        | /             # divisor operator
                        | [^\\\n"'/]*   # not string and backslash and newline
                    )+                  # one or more
                )*                      # zero or more
            )?                          # zero or one
        )
        """, re.VERBOSE | re.MULTILINE)
datatype = re.compile(r"""
        void
        | char
        | short
        | int
        | long
        | long[ ]int
        | long[ ]long
        | long[ ]long[ ]int
        | float
        | double
        | long[ ]double
        | _Bool
        """, re.VERBOSE)
keyword = re.compile(r"""
        (
            struct      # define type
            | union
            | enum
            | typedef   # typedef
            | extern    # extern
            | for       # loop
            | while
            | do
            | break
            | continue
            | if        # condition
            | else
            | switch
            | case
            | default
            | goto
            | const     # restrict
            | restrict
            | static
            | register
            | auto
            | unsigned
            | signed
            | volatile
            | _Atomic   # addition
            | _Complex
            | _Generic
            | _Imaginary
            | _Noreturn
            | _Static_assert
            | _Thread_local
            | inline    # inline
            | return    # return
            | sizeof    # sizeof
            | typeof    # typeof # gcc grammar
            | _Alignof  # alignof
        )
        """, re.VERBOSE)
quotesDouble = re.compile("\"")
quotesSingle = re.compile("\'")
floating = re.compile(r"""
        [0-9]+\.[0-9]+[fF]?             # decimal floating
        | 0x[0-9A-Fa-f]+\.[0-9A-Fa-f]+[fF]?p[0-9]+    # hexadecimal floating
        """, re.VERBOSE)
integer = re.compile(r"""
        0x[0-9A-Fa-f]+[Uu]?[Ll]{0,2}    # hexadecimal
        | 0[0-7]+[Uu]?[Ll]{0,2}         # octal
        | [1-9][0-9]*[Uu]?[Ll]{0,2}     # decimal
        | 0                             # 0
        """, re.VERBOSE)
operator = re.compile(r"""
        -> | \.                             # member
        | = | \+= | -= | \*= | /= | %=      # assignment
        | &= | \|= | \^= | <<= | >>= 
        | << | >>                           # bitwise shift
        | == | != | >= | <= | > | <         # comparison / relational
        | ! | && | \|\|                     # logical
        | ~ | & | \| | \^                   # bitwise (& also is address-of)
        | \+\+ | -- | \+ | - | \* | / | %   # arithmetic (* also is indirection)
        | \? | :                            # ternary conditional
        """, re.VERBOSE)
comma = re.compile(",")
identifier = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")
parenthesisOpen = re.compile(r"\(")
parenthesisClose = re.compile(r"\)")
braceOpen = re.compile(r"\{")
braceClose = re.compile(r"\}")
bracketOpen = re.compile(r"\[")
bracketClose = re.compile(r"\]")
semicolon = re.compile(";")
backslash = re.compile(r"\\")
newline = re.compile(r"\n")
etcCharators = re.compile(r"""
        @ | \#\# | \# | $ | % | ` | ~
        """, re.VERBOSE)


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


#  def match(text, regexList):
    
    #  for regex in regexList:
        #  if regex.matched



def scan(rawdata):
    tokens = []
    debug = ""
    line_cnt = 0
    line_nr = 0
    tmp = 0
    token_nr = 0

    preprocesses = []
    #  preprocesses = preprocess.findall(rawdata)
    
    # return preprocesses

    #  for key in preprocesses:
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
        #  print(lines)

        matchedString = preprocess.match(lines) # make matchedString as preprocess
                                                # about lines
        lines = ""                              # re-initialize 0
        if matchedString is None:               # if it is not preprocess
                                                # go to next line
            continue

        key = (matchedString.group(2), matchedString.group(3))
        print (str(line_nr) + " : " + str(key))
        if key[0] == "include":
            matchedString = re.compile('[ \t]?([<"])(.*)[>"]').search(key[1])

            if matchedString.group(1) == "<":
                token = Token(line=lines, line_nr=line_nr
                        , substance=matchedString.group(2), kind="T_INCLUDE_STD_H")
                tokens.append(token)
            elif matchedString.group(1) == '"':
                token = Token(line=lines, line_nr=line_nr
                        , substance=matchedString.group(2), kind="T_INCLUDE_USR_H")
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
                    , substance=None, kind="T_PREPROCESS_"+key[0].upper())
            tokens.append(token)
            continue
        elif key[0] == "elif":
            pass
        elif key[0] == "endif":
            token = Token(line=line, line_nr=line_nr
                    , substance=None, kind="T_PREPROCESS_"+key[0].upper())
            tokens.append(token)
            continue
        elif key[0] == "define":
            if key[1][0] == '(':
                key[0] = "definefunc"
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
                , substance=None, kind="T_PREPROCESS_"+key[0].upper())
        tokens.append(token)

        text = key[1]
        #  if len(tokens) > 0:
            #  token = Token("T_NEWLINE")
            #  tokens.append(token)
            # tokens.append((None, None, None, "T_NEWLINE"))
        while len(text) > 0:

            #  for regex in regexList:
                #  matchedString = regex[0].match(text)
                #  if matchedString is not None:
                    #  text = text[matchedString.end():]
                    #  if regex[0] == space:
                        #  continue
                        
                    #  token = Token(regex[1], line, line_nr, matchedString.group)
                    #  tokens.append(token)
                    #  continue

            matchedString = space.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                if matchedString.group() == "\n":
                    token = Token("T_NEWLINE")
                    tokens.append(token)
                continue

            matchedString = commentSingleLine.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token("T_COMMENT_SINGL_LINE")
                tokens.append(token)
                continue

            matchedString = commentMultiLineOpen.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token("T_COMMENT_MULTI_LINE_OPEN")
                tokens.append(token)
                continue

            matchedString = commentMultiLineClose.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token("T_COMMENT_MULTI_LINE_CLOSE")
                tokens.append(token)
                continue

            #  matchedString = preprocess.match(text)
            #  if matchedString is not None:
                #  text = text[matchedString.end():]
                #  token = Token(kind="T_PREPROCESS", line=line
                        #  , line_nr=line_nr, substance=(matchedString.group(1), matchedStirng.group(2)))
                #  tokens.append(token)
                #  continue

            # if text is matched identifier it is possible enough to be keyword
            # and datatype because they are matched by regular expression
            # [a-zA-Z_][a-zA-Z0-9_]*
            matchedString = identifier.match(text)
            if matchedString is not None:
                datatypeString = datatype.match(text)
                keywordString = keyword.match(text)
                if (datatypeString is not None 
                        and datatypeString.group() == matchedString.group()):
                    token = Token(line=None, line_nr=None
                            , substance=matchedString.group(), kind="T_DATATYPE")
                elif (keywordString is not None
                        and keywordString.group() == matchedString.group()):
                    token = Token(line=None, line_nr=None
                            , substance=matchedString.group(), kind="T_KEYWORD")
                else:
                    token = Token(line=line, line_nr=line_nr
                            , substance=matchedString.group(), kind="T_IDENTIFIER")
                text = text[matchedString.end():]
                #  token = Token(line=line, line_nr=line_nr
                        #  , substance=matchedString.group(), kind="T_IDENTIFIER")
                tokens.append(token)
                continue

            #  matchedString = datatype.match(text)
            #  if matchedString is not None:
                #  text = text[matchedString.end():]
                #  token = Token(line=None, line_nr=None
                        #  , substance=matchedString.group(), kind="T_DATATYPE")
                #  tokens.append(token)
                #  continue

            #  matchedString = keyword.match(text)
            #  if matchedString is not None:
                #  text = text[matchedString.end():]
                #  token = Token(line=None, line_nr=None
                        #  , substance=matchedString.group(), kind="T_KEYWORD")
                #  tokens.append(token)
                #  continue

            matchedString = quotesDouble.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=None
                        , substance=matchedString.group(), kind="T_QUOTES_DOUBLE")
                tokens.append(token)
                continue

            matchedString = quotesSingle.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=None
                        , substance=matchedString.group(), kind="T_QUOTES_SINGLE")
                tokens.append(token)
                continue

            matchedString = floating.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=None
                        , substance=matchedString.group(), kind="T_FLOATING")
                tokens.append(token)
                continue

            matchedString = integer.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=None
                        , substance=matchedString.group(), kind="T_INTEGER")
                tokens.append(token)
                continue

            matchedString = operator.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=None
                        , substance=matchedString.group(), kind="T_OPERATOR")
                tokens.append(token)
                continue

            matchedString = comma.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=None
                        , substance=matchedString.group(), kind="T_COMMA")
                tokens.append(token)
                continue

            matchedString = parenthesisOpen.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=line_nr
                        , substance=None, kind="T_PARENTHESIS_OPEN")
                tokens.append(token)
                continue

            matchedString = parenthesisClose.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=line_nr
                        , substance=None, kind="T_PARENTHESIS_CLOSE")
                tokens.append(token)
                continue

            matchedString = braceOpen.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=line_nr
                        , substance=None, kind="T_BRACE_OPEN")
                tokens.append(token)
                continue

            matchedString = braceClose.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=line_nr
                        , substance=None, kind="T_BRACE_CLOSE")
                tokens.append(token)
                continue

            matchedString = bracketOpen.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=line_nr
                        , substance=None, kind="T_BRACKET_OPEN")
                tokens.append(token)
                continue

            matchedString = bracketClose.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=line_nr
                        , substance=None, kind="T_BRACKET_CLOSE")
                tokens.append(token)
                continue

            matchedString = semicolon.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=line_nr
                        , substance=matchedString.group(), kind="T_SEMICOLON")
                tokens.append(token)
                continue

            matchedString = backslash.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=None
                        , substance=matchedString.group(), kind="T_BACKSLASH")
                tokens.append(token)
                continue

            matchedString = etcCharators.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                token = Token(line=None, line_nr=None
                        , substance=matchedString.group(), kind="T_ETC_CHARATORS")
                tokens.append(token)
                continue

            print(line_nr, end=': ')
            print(text)
            raise AssertionError("CscannerNoMatchError")

    return tokens               # scanner test
    #return cp.parse(tokens)    # parser test

