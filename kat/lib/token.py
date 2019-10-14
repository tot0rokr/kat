from kat.tracer.tokenlib            import token_kind_index as c_token_kind_index
from kat.tracer.cc_tokenlib         import token_kind_index as cc_token_kind_index
class Token:
    def __init__(self, kind, substance=None, line_nr=None, line=None):
        self.kind = kind
        self.line = line
        self.line_nr = line_nr
        self.substance = substance

    def __call__(self):
        return c_token_kind_index[self.kind]

    def __str__(self):
        return str((c_token_kind_index[self.kind], self.line, self.line_nr, self.substance))

class CurConfigToken(Token):
    def __call__(self):
        return cc_token_kind_index[self.kind]

    def __str__(self):
        return str((cc_token_kind_index[self.kind], self.line, self.line_nr, self.substance))
