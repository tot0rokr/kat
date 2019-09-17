"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io

cscanner.py

return: tuple(line, line_nr, unit, token)
line: a line of token
line_nr: a number of line
unit: a name of minimum unit of line
token: a semantic type of unit processed by scanner


tokens:
    T_NEWLINE
    T_COMMENT_SINGL_LINE
    T_COMMENT_MULTI_LINE_OPEN
    T_COMMENT_MULTI_LINE_CLOSE
    T_PREPROCESS
    T_DATATYPE
    T_KEYWORD
    T_STRING
    T_CHARACTOR
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

space = re.compile("[ \t\r\n\v\f]") # equal with \s
commentSingleLine = re.compile(r"//.*")
commentMultiLineOpen = re.compile(r"/\*")
commentMultiLineClose = re.compile(r"\*/")
#  unsigned = re.compile("unsigned")
preprocess = re.compile(r"""
        \#                  # prefix
        (
            include[ \t]?[<"](.*)[>"]
            | # (
                define
                | if
                | ifdef
                | ifndef
                | else
                | elif
                | endif
                | error
                | undef
                | pragma
                | warning
                | line
                | defined
            #  )[ \t][^\\\n]*(\\\n[^\\\n]*)*   # several lines
        )
        """, re.VERBOSE)
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
        = | \+= | -= | \*= | /= | %=
        | &= | \|= | \^= | <<= | >>= 
        | == | != | >= | <= | > | <
        | \+\+ | -- | \+ | -
        | \* | / | %
        | ! | && | \|\| 
        | ~ | & | \| | \^ | << | >>
        | -> | \. 
        | \? | :
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
etcCharators = re.compile(r"""
        @ | \# | $ | % | ` | ~
        """, re.VERBOSE)




def scan(rawdata):
    tokens = []
    debug = ""
    line_nr = 0
    token_nr = 0
    for line in rawdata.split("\n"):
        if len(tokens) > 0:
            tokens.append((None, None, None, "T_NEWLINE"))
        line_nr = line_nr + 1
        text = line
        while len(text) > 0:

            matchedString = space.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                continue

            matchedString = commentSingleLine.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, None, "T_COMMENT_SINGL_LINE"))
                continue

            matchedString = commentMultiLineOpen.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, None, "T_COMMENT_MULTI_LINE_OPEN"))
                continue

            matchedString = commentMultiLineClose.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, None, "T_COMMENT_MULTI_LINE_CLOSE"))
                continue

            matchedString = preprocess.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((line, line_nr, matchedString.group(1), "T_PREPROCESS"))
                continue

            matchedString = datatype.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_DATATYPE"))
                continue

            matchedString = keyword.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_KEYWORD"))
                continue

            matchedString = quotesDouble.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_QUOTES_DOUBLE"))
                continue

            matchedString = quotesSingle.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_QUOTES_SINGLE"))
                continue

            matchedString = floating.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_FLOATING"))
                continue

            matchedString = integer.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_INTEGER"))
                continue

            matchedString = operator.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_OPERATOR"))
                continue

            matchedString = comma.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_COMMA"))
                continue

            matchedString = identifier.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((line, line_nr, matchedString.group(), "T_IDENTIFIER"))
                continue

            matchedString = parenthesisOpen.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, line_nr, matchedString.group(), "T_PARENTHESIS_OPEN"))
                continue

            matchedString = parenthesisClose.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, line_nr, matchedString.group(), "T_PARENTHESIS_CLOSE"))
                continue

            matchedString = braceOpen.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, line_nr, matchedString.group(), "T_BRACE_OPEN"))
                continue

            matchedString = braceClose.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, line_nr, matchedString.group(), "T_BRACE_CLOSE"))
                continue

            matchedString = bracketOpen.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, line_nr, matchedString.group(), "T_BRACKET_OPEN"))
                continue

            matchedString = bracketClose.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, line_nr, matchedString.group(), "T_BRACKET_CLOSE"))
                continue

            matchedString = semicolon.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, line_nr, matchedString.group(), "T_SEMICOLON"))
                continue

            matchedString = backslash.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_BACKSLASH"))
                continue

            matchedString = etcCharators.match(text)
            if matchedString is not None:
                text = text[matchedString.end():]
                tokens.append((None, None, matchedString.group(), "T_ETC_CHARATORS"))
                continue

            print(line_nr, end=': ')
            print(text)
            raise AssertionError("CscannerNoMatchError")

    return tokens               # scanner test
    #return cp.parse(tokens)    # parser test

