import re
import operator as op

regex = []

space = re.compile("[ \t\r\n\v\f]")
regex.append(space)
comment = re.compile("#.*")
regex.append(comment)
identifier = re.compile(r"CONFIG_([a-zA-Z0-9_]*)")
regex.append(identifier)
#  keyword = re.compile(r"""
        #  CONFIG_         # Config prefix
        #  """, re.VERBOSE)
word = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")
regex.append(word)
string = re.compile("\".*\"")
regex.append(string)
number = re.compile(r"""
        0x[0-9A-Fa-f]+[Uu]?[Ll]{0,2}    # hexadecimal
        | 0[0-7]+[Uu]?[Ll]{0,2}         # octal
        | [1-9][0-9]*[Uu]?[Ll]{0,2}     # decimal
        | 0                             # 0
        """, re.VERBOSE)
regex.append(number)
operator = re.compile("=")
regex.append(operator)




it = range(100).__iter__()
token_kind = {}
token_kind['T_FIRST'] = it.__next__()
token_kind['T_COMMENT'] = it.__next__()         # nothing
token_kind['T_IDENTIFIER'] = it.__next__()
token_kind['T_WORD'] = it.__next__()
token_kind['T_STRING'] = it.__next__()
token_kind['T_NUMBER'] = it.__next__()
token_kind['T_OPERATOR'] = it.__next__()
token_kind['T_LAST'] = it.__next__()


token_kind_index = []
for it in sorted(token_kind.items(), key=op.itemgetter(1)):
    token_kind_index.append(it[0])

