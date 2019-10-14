"""
Author: TOT0Ro (tot0roprog@gmail.com)
        tot0rokr.github.io       

curconfigparser.py

tokens: Result of lexical analysis about ".config" file
return: constructed tags

"""

from kat.tracer.cc_tokenlib import *
from kat.lib.token          import CurConfigToken
from kat.lib.tag            import CurConfigTag

def parse(tokens):
    state = "start"
    tag = {}
    tags = []

    tokens.append(CurConfigToken(token_kind['T_LAST']))      # This is only used by last chunk

    error_text = None

    tokens.reverse()

    if tokens.pop().kind != token_kind['T_FIRST']:
        raise AssertionError("ccparser.py: Error initialized tokens")

    def start():
        while True:
            if tokens[-1].kind == token_kind['T_LAST']:
                return tags
            
            elif tokens[-1].kind == token_kind['T_IDENTIFIER']:
                tok = tokens.pop()
                tag = CurConfigTag(name=tok.substance, line=tok.line_nr)
                expr = expression()
                tag.value = expr
                tags.append(tag)

            else:
                error_text = "start"
                raise AssertionError(error_text)

    def expression():
        expr = None
        if tokens[-1].kind == token_kind['T_WORD']:
            tok = tokens.pop()
            expr = tok.substance
        elif tokens[-1].kind == token_kind['T_STRING']:
            tok = tokens.pop()
            expr = tok.substance
        elif tokens[-1].kind == token_kind['T_NUMBER']:
            tok = tokens.pop()
            if '0x' in tok.substance:
                expr = int(tok.substance, 16)
            else:
                expr = int(tok.substance)
        else:
            error_text = "expression"
            raise AssertionError(error_text)
        return expr

    return start()


