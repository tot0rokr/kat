from kat.lib.scope      import Scope
class Contents:
    def __init__(self, text, type):
        self.text = None            # contents
        self.type = None            # what it is tag type.

    def __call__(self):
        return self.text

