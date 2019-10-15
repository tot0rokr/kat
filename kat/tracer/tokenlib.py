import re
import operator as op


regex = []

# space
space = re.compile("[ \t\r\v\f]") # equal with \s except \n
regex.append(space)
newline = re.compile("\n")
regex.append(newline)

# comment
commentSingleLine = re.compile(r"//")
regex.append(commentSingleLine)
commentMultiLineOpen = re.compile(r"/\*")
regex.append(commentMultiLineOpen)
commentMultiLineClose = re.compile(r"\*/")
regex.append(commentMultiLineClose)

# preprocess
preprocess = re.compile(r"""
        ^\#                  # prefix
        (
            [ \t]*
            (
                #  [a-z]+              # preprocess word
                include | define | ifndef | ifdef | if | elif | else
                | endif | error | undef | pragma | warning | line
            ) 
            (
                (
                    [ \t]+                  # space TOTO: away
                    (
                        /\*(.|\n|[^*]/)*\*/            # multi line comment
                        | "(\\.|.)*"              # string value
                        | '(\\.|.)'               # charactor value
                        #  | ".*"          # string value
                        #  | '.'           # charactor value
                        | //.*[^\n]
                        | /                 # divisor operator
                        #  | [^\\\n/]*       # not string and backslash and newline
                        | [^\\\n'"/]*
                    )+                      # one or more
                    (
                        \\[ \t]*\n          # backslash - several space - newline
                        (
                            /\*(.|\n|[^*]/)*\*/        # multi line comment
                            #  | ".*"          # string value
                            #  | '.'           # charactor value
                            | "(\\.|.)*"              # string value
                            | '(\\.|.)'               # charactor value
                            | //.*[^\n]
                            | /             # divisor operator
                            #  | [^\\\n/]*   # not string and backslash and newline
                            | [^\\\n'"/]*
                        )*                  # one or more
                    )*                      # zero or more
                )?                          # zero or one
                [ \t]*\n                          # last newline
            )
        )
        """, re.VERBOSE | re.MULTILINE)
regex.append(preprocess)

# similar word
identifier = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")
regex.append(identifier)
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
regex.append(datatype)
userdefinetype = re.compile(r"""
            struct      # define type
            | union
            | enum
        """, re.VERBOSE)
regex.append(userdefinetype)
typedef = re.compile(r"typedef")
regex.append(typedef)
loop = re.compile(r"""
            for       # loop
            | while
            | do
        """, re.VERBOSE)
regex.append(loop)
loopcontrol = re.compile(r"""
            break
            | continue
        """, re.VERBOSE)
regex.append(loopcontrol)
condition = re.compile(r"""
            if        # condition
            | else
            | else[ \t]+if
        """, re.VERBOSE)
regex.append(condition)
switch = re.compile(r"switch")
regex.append(switch)
case = re.compile(r"case")
regex.append(case)
default = re.compile(r"default")
regex.append(default)
goto = re.compile(r"goto")
regex.append(goto)
type_qualifier = re.compile(r"""
            const     # restrict
            | restrict
            | volatile
        """, re.VERBOSE)
regex.append(type_qualifier)
type_specifier = re.compile(r"""
            signed
            | unsigned
        """, re.VERBOSE)
regex.append(type_specifier)
storage_class_specifier = re.compile(r"""
            extern
            | register
            | static
            | auto
        """, re.VERBOSE)
regex.append(storage_class_specifier)
inline = re.compile(r"inline")
regex.append(inline)
return_ = re.compile(r"return")
regex.append(return_)
typeof = re.compile(r"typeof")
regex.append(typeof)
sizeof = re.compile(r"sizeof")
regex.append(sizeof)
#  keyword = re.compile(r"""
        #  (
            #  #_Atomic   # addition
            #  #| _Complex
            #  #| _Generic
            #  #| _Imaginary
            #  #| _Noreturn
            #  #| _Static_assert
            #  #| _Thread_local
            #  | sizeof    # sizeof
            #  | typeof    # typeof # gcc grammar
            #  #| _Alignof  # alignof
        #  )
        #  """, re.VERBOSE)

# Numeric
floating = re.compile(r"""
        [0-9]+\.[0-9]+[fF]?             # decimal floating
        | 0x[0-9A-Fa-f]+\.[0-9A-Fa-f]+[fF]?p[0-9]+    # hexadecimal floating
        """, re.VERBOSE)
regex.append(floating)
integer = re.compile(r"""
        0x[0-9A-Fa-f]+[Uu]?[Ll]{0,2}    # hexadecimal
        | 0[0-7]+[Uu]?[Ll]{0,2}         # octal
        | [1-9][0-9]*[Uu]?[Ll]{0,2}     # decimal
        | 0                             # 0
        """, re.VERBOSE)
regex.append(integer)

# special charactor
quotesDouble = re.compile(r"\"")
regex.append(quotesDouble)
quotesSingle = re.compile(r"\'")
regex.append(quotesSingle)
variable_arguments = re.compile(r"\.\.\.")
regex.append(variable_arguments)
operator = re.compile(r"""
        -> | \.                             # member
        | = | \+= | -= | \*= | /= | %=      # assignment
        | &= | \|= | \^= | <<= | >>= 
        | << | >>                           # bitwise shift
        | == | != | >= | <= | > | <         # comparison / relational
        | ! | && | \|\|                     # logical
        | ~ | & | \| | \^                   # bitwise (& also is address-of)
        | \+\+ | -- | \+ | - | \* | / | %   # arithmetic (* also is indirection)
        | \?                                # ternary conditional
        """, re.VERBOSE)
regex.append(operator)
comma = re.compile(",")
regex.append(comma)
colon = re.compile(":")
regex.append(colon)
parenthesisOpen = re.compile(r"\(")
regex.append(parenthesisOpen)
parenthesisClose = re.compile(r"\)")
regex.append(parenthesisClose)
braceOpen = re.compile(r"\{")
regex.append(braceOpen)
braceClose = re.compile(r"\}")
regex.append(braceClose)
bracketOpen = re.compile(r"\[")
regex.append(bracketOpen)
bracketClose = re.compile(r"\]")
regex.append(bracketClose)
semicolon = re.compile(";")
regex.append(semicolon)
char_backslash = re.compile(r"\\\\")
regex.append(char_backslash)
char_quotes_double = re.compile(r"\\\"")
regex.append(char_quotes_double)
char_quotes_single = re.compile(r"\\\'")
regex.append(char_quotes_single)
backslash = re.compile(r"\\")
regex.append(backslash)
#  newline = re.compile(r"\n")
etcCharators = re.compile(r"""
        @ | \#\# | \# | \$ | % | ` | ~
        """, re.VERBOSE)
regex.append(etcCharators)


it = range(100).__iter__() # 100 is just over number of token_kind
token_kind = {}
token_kind['T_FIRST'] = it.__next__()

# space
token_kind['T_NEWLINE'] = it.__next__()

# comment
token_kind['T_COMMENT_SINGL_LINE'] = it.__next__()        # //
token_kind['T_COMMENT_MULTI_LINE_OPEN'] = it.__next__()   # /*
token_kind['T_COMMENT_MULTI_LINE_CLOSE'] = it.__next__()  # */

# preprocess
token_kind['T_PREPROCESS'] = it.__next__()                # like #include ...

# similar word
token_kind['T_IDENTIFIER'] = it.__next__()
token_kind['T_DATATYPE'] = it.__next__()                  # like int, long ...
token_kind['T_USERDEFINEDTYPE'] = it.__next__()           # struct, union, enum
token_kind['T_TYPEDEF'] = it.__next__()                   # typedef
token_kind['T_LOOP'] = it.__next__()                      # like for, while ...
token_kind['T_LOOP_CONTROL'] = it.__next__()              # break, continue
token_kind['T_CONDITION'] = it.__next__()                 # if, else
token_kind['T_SWITCH'] = it.__next__()                    # switch
token_kind['T_CASE'] = it.__next__()                      # case
token_kind['T_DEFAULT'] = it.__next__()                   # default
token_kind['T_GOTO'] = it.__next__()                      # goto
token_kind['T_TYPE_QUALIFIER'] = it.__next__()            # const, restrict, volatile
token_kind['T_TYPE_SPECIFIER'] = it.__next__()            # signed, unsigned
token_kind['T_STORAGE_CLASS_SPECIFIER'] = it.__next__()   # like extern, static ...
token_kind['T_INLINE'] = it.__next__()                    # inline
token_kind['T_RETURN'] = it.__next__()                    # return
token_kind['T_TYPEOF'] = it.__next__()                    # typeof
token_kind['T_SIZEOF'] = it.__next__()                    # sizeof

# Numeric
token_kind['T_FLOATING'] = it.__next__()
token_kind['T_INTEGER'] = it.__next__()

# special charactor
token_kind['T_QUOTES_DOUBLE'] = it.__next__()             # "
token_kind['T_QUOTES_SINGLE'] = it.__next__()             # '
token_kind['T_VARIABLE_ARGUMENTS'] = it.__next__()        # ...
token_kind['T_OPERATOR'] = it.__next__()                  # all of operator
token_kind['T_COMMA'] = it.__next__()                     # ,
token_kind['T_COLON'] = it.__next__()                     # :
token_kind['T_PARENTHESIS_OPEN'] = it.__next__()          # (
token_kind['T_PARENTHESIS_CLOSE'] = it.__next__()         # )
token_kind['T_BRACE_OPEN'] = it.__next__()                # {
token_kind['T_BRACE_CLOSE'] = it.__next__()               # }
token_kind['T_BRACKET_OPEN'] = it.__next__()              # [
token_kind['T_BRACKET_CLOSE'] = it.__next__()             # ]
token_kind['T_SEMICOLON'] = it.__next__()                 # ;
token_kind['T_CHAR_BACKSLASH'] = it.__next__()                 # \\
token_kind['T_CHAR_QUOTES_DOUBLE'] = it.__next__()                 # \"
token_kind['T_CHAR_QUOTES_SINGLE'] = it.__next__()                 # \'
token_kind['T_BACKSLASH'] = it.__next__()                 # \
token_kind['T_ETC'] = it.__next__()                       # @, ##, #, $, %, `, ~


token_kind['T_LAST'] = it.__next__()

# preprocess addition
token_kind['T_INCLUDE_STD_H'] = it.__next__()
token_kind['T_INCLUDE_USR_H'] = it.__next__()
token_kind['T_INCLUDE_MACRO'] = it.__next__()

token_kind_index = []
for it in sorted(token_kind.items(), key=op.itemgetter(1)):
    token_kind_index.append(it[0])


it = range(100).__iter__()
preprocess_kind = {}
preprocess_kind['if'] = it.__next__()
preprocess_kind['ifdef'] = it.__next__()
preprocess_kind['ifndef'] = it.__next__()
preprocess_kind['else'] = it.__next__()
preprocess_kind['elif'] = it.__next__()
preprocess_kind['endif'] = it.__next__()
preprocess_kind['macro'] = it.__next__()
preprocess_kind['macrofunc'] = it.__next__()
preprocess_kind['error'] = it.__next__()
preprocess_kind['undef'] = it.__next__()
preprocess_kind['pragma'] = it.__next__()
preprocess_kind['warning'] = it.__next__()
preprocess_kind['line'] = it.__next__()

preprocess_kind_index = []
for it in sorted(preprocess_kind.items(), key=op.itemgetter(1)):
    preprocess_kind_index.append(it[0])
