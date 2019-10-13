from kat.tracer.pplib   import *
class Token:
    def __init__(self, kind, substance=None, line_nr=None, line=None):
        self.kind = kind
        self.line = line
        self.line_nr = line_nr
        self.substance = substance

    def __call__(self):
        return token_kind_index[self.kind]

    def __str__(self):
        return str((token_kind_index[self.kind], self.line, self.line_nr, self.substance))
