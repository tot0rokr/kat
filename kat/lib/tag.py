from kat.lib.scope      import Scope
from kat.lib.contents   import Contents
from kat.lib.file       import File

class Tag:
    def __init__(self, name, line, defi=None):
        self.name = name
        self.line = line
        self.defi = defi

    def __str__(self):
        return str((self.name, self.line))
    

class CurConfigTag(Tag): # curconfig tag
    def __init__(self, name, line, value=None):
        super().__init__(name, line)
        self.value = value

    def __repr__(self):
        return repr(self.name)

    def __str__(self):
        return str((self.name, self.line, self.value))

class MacroTag(Tag):
    def __init__(self, path, line, name, scope, type=None):
        super().__init__(name, line, self)
        self.path = path               # File() / file path
        #  self.contents = Contents()     # Contents
        self.contained_by = scope
        self.type = type                 # what it is used type in code

    def __repr__(self):
        return repr(self.name)

    def __str__(self):
        return str((self.name, self.line, self.path))


class DefinitionTag(Tag):
    def __init__(self, path, line, name, scope, type=None):
        self.super(name, line, self)
        self.validScope = scope                   # ScopeTag() / valid scope. 


class ScopeTag(Tag):
    def __init__(self, path, line, scope, name="anony", type=""):
        self.super(path, line, name)
        self.scope = Scope(line)
        

