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
from kat.lib.scope      import *
from kat.tracer.tokenlib   import *
import re


def parse(tokens, file_tag):
    scope_stack = []
    tags = []
    include_files = []                   # included libraries
                                        # they'll be mapped by pptracer after
                                        # returning this function
    included_scope = []

    path = file_tag.path
    base = file_tag.scope
    scope_stack.append(base)

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
                include_files.append(tokens.pop().substance)

            elif tokens[-1].kind == token_kind['T_INCLUDE_USR_H']:
                print(path + "Is it exist? " + tokens.pop().substance)
                raise AssertionError("ppparser: include user header: " + path)
                include_files.append(tokens.pop().substance)

            elif tokens[-1].kind == token_kind['T_PREPROCESS']:
                tok = tokens.pop()
                if tok.substance == preprocess_kind['macro']:
                    macro()

                elif tok.substance == preprocess_kind['macrofunc']:
                    macrofunc()

                elif tok.substance == preprocess_kind['undef']:
                    macroundef()

                elif tok.substance == preprocess_kind['ifdef']:
                    ppifdef(tok.line_nr)

                elif tok.substance == preprocess_kind['ifndef']:
                    ppifndef(tok.line_nr)

                elif tok.substance == preprocess_kind['if']:
                    ppif(tok.line_nr)

                elif tok.substance == preprocess_kind['elif']:
                    ppelif(tok.line_nr)

                elif tok.substance == preprocess_kind['else']:
                    ppelse(tok.line_nr)

                elif tok.substance == preprocess_kind['endif']:
                    ppendif(tok.line_nr)

                # pass preprocess
                elif tok.substance == preprocess_kind['pragma']:
                    expression("pass")
                elif tok.substance == preprocess_kind['error']:
                    expression("pass")
                elif tok.substance == preprocess_kind['line']:
                    expression("pass")
                elif tok.substance == preprocess_kind['warning']:
                    expression("pass")

            elif tokens[-1].kind == token_kind['T_LAST']:
                return (tags, include_files, included_scope)

            else:
                raise AssertionError("error_start")
                #  expression("start")
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
                    , scope=scope_stack[-1], type="macro")
            expr = expression("macro")
            # TODO: put {expr} in {tag}
            file_tag.append_defined_tag(tag.name)
            tags.append(tag)
        else:
            error_text = "macro"
            raise AssertionError(error_text)

    def macrofunc():
        if tokens[-1].kind == token_kind['T_IDENTIFIER']:
            tok = tokens.pop()
            tag = MacroTag(name=tok.substance, line=tok.line_nr, path=path
                    , scope=scope_stack[-1], type="macrofunc")
            argu_list = macrofunc_argu()
            # TODO: put {argu_list} in {tag}
            expr = expression("macro")
            # TODO: put {expr} in {tag}
            file_tag.append_defined_tag(tag.name)
            tags.append(tag)
        else:
            error_text = "macrofunc"
            raise AssertionError(error_text)

    def macroundef():
        if tokens[-1].kind == token_kind['T_IDENTIFIER']:
            tok = tokens.pop()
            tag = MacroTag(name=tok.substance, line=tok.line_nr, path=path
                    , scope=scope_stack[-1], type="undef")
            file_tag.append_defined_tag(tag.name)
            tags.append(tag)
        else:
            error_text = "macroundef"
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

        elif type == "start":
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

        elif type == "ppif":
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
                        error_text = "expression - ppif"
                        raise AssertionError(error_text)
                else:
                    tokens.pop()
            return expr

        elif type == "pass":
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



    def ppifdef(line_nr):
        if tokens[-1].kind == token_kind['T_IDENTIFIER']:
            tok = tokens.pop()
            scope = PreprocessScope(path=file_tag, scope=scope_stack[-1], start=line_nr)
            scope.condition = [tok.substance, 1, "=="]
            scope_stack.append(scope)
        else:
            error_text = "ppifdef"
            raise AssertionError(error_text)

    def ppifndef(line_nr):
        if tokens[-1].kind == token_kind['T_IDENTIFIER']:
            tok = tokens.pop()
            scope = PreprocessScope(path=file_tag, scope=scope_stack[-1], start=line_nr)
            scope.condition = [tok.substance, 1, "!="]
            scope_stack.append(scope)
        else:
            error_text = "ppifndef"
            raise AssertionError(error_text)

    def ppif(line_nr):
        expr = expression("ppif")
        scope = PreprocessScope(path=file_tag, scope=scope_stack[-1], start=line_nr)
        scope.condition = expr
        scope_stack.append(scope)

    def ppelif(line_nr):
        pre_scope = scope_stack.pop()
        pre_scope.line[1] = line_nr - 1
        expr = expression("ppif") # expression of ppelif is same
        scope = PreprocessScope(path=file_tag, scope=pre_scope.contained_by, start=line_nr)
        scope.condition = expr
        pre_scope.post_associator = scope
        scope.pre_associator = pre_scope
        scope_stack.append(scope)
        included_scope.append(pre_scope)

        
    def ppelse(line_nr):
        pre_scope = scope_stack.pop()
        pre_scope.line[1] = line_nr - 1
        scope = PreprocessScope(path=file_tag, scope=pre_scope.contained_by, start=line_nr)
        pre_scope.post_associator = scope
        scope.pre_associator = pre_scope
        scope_stack.append(scope)
        included_scope.append(pre_scope)

    def ppendif(line_nr):
        pre_scope = scope_stack.pop()
        pre_scope.line[1] = line_nr - 1
        included_scope.append(pre_scope)
        

    return start()


