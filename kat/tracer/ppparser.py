"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io       

ppparser.py
    preprocess parser

tokens: Result of lexical analysis about preprocesses in "*.c" c code
return: constructed tags

"""


from kat.lib.tag        import *
from kat.lib.file       import File
from kat.lib.token      import Token
from kat.lib.scope      import Scope
from kat.tracer.pplib   import *
import re


def parse(tokens, file_tag):
    scope = []
    stack = []
    tags = []
    include_files = []                   # included libraries
                                        # they'll be mapped by pptracer after
                                        # returning this function

    path = file_tag.path
    base = file_tag.scope
    scope.append(base)

    tokens.append(Token(token_kind['T_LAST']))      # This is only used by last chunk

    #  def shift(from, to, symbol, state):
        #  to.append(from.pop(0))
        
    #  def pop(list):
        #  list.pop(0)

    error_text = None

    tokens.reverse()

    if tokens.pop().kind != token_kind['T_FIRST']:
        raise AssertionError("Error initialized tokens")

    def start():
        while True:
            if tokens[-1].kind == token_kind['T_NEWLINE']:
                tokens.pop()


            elif tokens[-1].kind == token_kind['T_COMMENT_SINGL_LINE']:
                tokens.pop()
                comment_single()

            elif tokens[-1].kind == token_kind['T_COMMENT_MULTI_LINE_OPEN']:
                tokens.pop()
                comment_multiline()

            elif tokens[-1].kind == token_kind['T_QUOTES_DOUBLE']:
                tokens.pop()
                string()

            elif tokens[-1].kind == token_kind['T_QUOTES_SINGLE']:
                tokens.pop()
                charactor()

            elif tokens[-1].kind == token_kind['T_INCLUDE_STD_H']:
                #  includeFilePath = re.compile(r"<(.*)>").search(token.substance).group(1)
                #  include_files.append(includeFilePath)
                #  include_files.append(tokens.pop().substance)
                tokens.pop().substance

            elif tokens[-1].kind == token_kind['T_INCLUDE_USR_H']:
                #  print(path + "Is it exist? " + tokens.pop().substance)
                tokens.pop().substance

            elif tokens[-1].kind == token_kind['T_PREPROCESS']:
                tok = tokens.pop()
                if tok.substance == preprocess_kind['macro']:
                    #  tokens.pop()
                    tag = macro()
                    file_tag.appendDefinedTag(tag.name)
                    tags.append(tag)

                elif tok.substance == preprocess_kind['macrofunc']:
                    #  tokens.pop()
                    tag = macrofunc()
                    file_tag.appendDefinedTag(tag.name)
                    tags.append(tag)
            #  elif tokens[-1].kind == token_kind['T_PREPROCESS_MACRO']: # finish
            #  elif tokens[-1].kind == token_kind['T_PREPROCESS_MACROFUNC']: #finish


            elif tokens[-1].kind == token_kind['T_LAST']:
                return (tags, include_files)

            else:
                expression("start")
                #  error_text = "start"
                #  break

    def comment_single():
        while True:
            if token[-1].kind == token_kind['T_NEWLINE']:
                tokens.pop()
                break
            else:
                tokens.pop()
        
    def comment_multiline():
        while True:
            if tokens[-1].kind == token_kind['T_COMMENT_MULTI_LINE_CLOSE']:
                tokens.pop()
                break
            else:
                tokens.pop()

    def string():
        data = ""
        while True:
            if tokens[-1].kind == token_kind['T_NEWLINE']:
                error_text = "string"
                raise AssertionError(error_text)
            elif tokens[-1].kind == token_kind['T_QUOTES_DOUBLE']:
                tokens.pop()
                break
            else:
                data += tokens.pop().substance
        return data
    
    def charactor():
        data = ""
        while True:
            if tokens[-1].kind == token_kind['T_NEWLINE']:
                error_text = "charactor_start"
                raise AssertionError(error_text)
            elif tokens[-1].kind == token_kind['T_QUOTES_SINGLE']:
                tokens.pop()
                break
            else:
                data = tokens.pop().substance
        return data

    def macro():
        if tokens[-1].kind == token_kind['T_IDENTIFIER']:
            tok = tokens.pop()
            tag = MacroTag(name=tok.substance, line=tok.line_nr, path=path
                    , scope=scope[-1], type="macro")
            expr = expression("macro")
            # TODO: put {expr} in {tag}
            return tag
        else:
            error_text = "macro"
            raise AssertionError(error_text)

    def macrofunc():
        if tokens[-1].kind == token_kind['T_IDENTIFIER']:
            tok = tokens.pop()
            tag = MacroTag(name=tok.substance, line=tok.line_nr, path=path
                    , scope=scope[-1], type="macrofunc")
            argu_list = macrofunc_argu()
            # TODO: put {argu_list} in {tag}
            expr = expression("macro")
            # TODO: put {expr} in {tag}
            return tag
            file_tag.appendDefinedTag(tag.name)
            tags.append(tag)
        else:
            error_text = "macrofunc"
            raise AssertionError(error_text)

    def macrofunc_argu():
        if tokens[-1].kind == token_kind['T_PARENTHESIS_OPEN']:
            tokens.pop()
            li = []
            if tokens[-1].kind == token_kind['T_IDENTIFIER']: # listing
                li.append(tokens.pop())
                while tokens[-1].kind == token_kind['T_COMMA']:
                    tokens.pop()
                    if tokens[-1].kind == token_kind['T_IDENTIFIER']:
                        li.append(tokens.pop())
                    elif tokens[-1].kind == token_kind['T_VARIABLE_ARGUMENTS']:
                        li.append(tokens.pop())
                        break
            elif tokens[-1].kind == token_kind['T_VARIABLE_ARGUMENTS']:
                li.append(tokens.pop())
            else:
                error_text = "macrofunc_argu - listing"
                raise AssertionError(error_text)

            if tokens[-1].kind == token_kind['T_PARENTHESIS_CLOSE']: # list end
                tokens.pop()
            else:
                error_text = "macrofunc_argu - list end"
                raise AssertionError(error_text)

            return li

        else:
            error_text = "macrofunc_argu"
            raise AssertionError(error_text)

    def expression(type):
        if type == "macro":
            expr = []
            while True:
                if tokens[-1].kind == token_kind['T_NEWLINE']:
                    tokens.pop()
                    break
                elif tokens[-1].kind == token_kind['T_QUOTES_DOUBLE']:
                    tokens.pop()
                    string()
                elif tokens[-1].kind == token_kind['T_QUOTES_SINGLE']:
                    tokens.pop()
                    charactor()
                elif tokens[-1].kind == token_kind['T_BACKSLASH']:
                    tokens.pop()
                    if tokens[-1].kind == token_kind['T_NEWLINE']:
                        tokens.pop()
                    else:
                        error_text = "expression - macro"
                        raise AssertionError(error_text)
                        break
                else:
                    # TODO: write what is in macro
                    expr = tokens.pop()
            return expr

        if type == "start":
            while True:
                if tokens[-1].kind == token_kind['T_NEWLINE']:
                    tokens.pop()
                    break
                elif tokens[-1].kind == token_kind['T_QUOTES_DOUBLE']:
                    tokens.pop()
                    string()
                elif tokens[-1].kind == token_kind['T_QUOTES_SINGLE']:
                    tokens.pop()
                    charactor()
                elif tokens[-1].kind == token_kind['T_BACKSLASH']:
                    tokens.pop()
                    if tokens[-1].kind == token_kind['T_NEWLINE']:
                        tokens.pop()
                    else:
                        error_text = "expression - start"
                        raise AssertionError(error_text)
                else:
                    tokens.pop()
            return None

        else:
            error_text = "expression"
            raise AssertionError(error_text)


        #  else:
            #  error_text = "undefined state"
            #  raise AssertionError(error_text)

    return start()

    #  print("state : {}".format(stack[-1]))
    #  print("token : {}".format(tokens[-1]))
    #  raise AssertionError("ppparser: " + error_text)

