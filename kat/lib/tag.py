from scope      import Scope
from contents   import Contents
from file       import File
class Tag:
    def __init__(self, path, line, name, scope, type=None, defi=None):
        self.path = path               # File() / file path
        self.line = line               # Int    / line number
        self.name = name                 # str()  / tag name
        self.contents = Contents()     # Contents
        self.container = scope
        self.type = type                 # what it is used type in code
        self.definition = defi             # DefinitionTag()  / definition tag

    def __repr__(self):
        return repr(self.name)

class DefineTag(Tag):
    def __init__(self, path, line, name, scope, type=None):



class DefinitionTag(Tag):
    def __init__(self, path, line, name, scope, type=None):
        self.super(path, line, name, type, self)
        self.validScope = scope                   # ScopeTag() / valid scope. 


class ScopeTag(Tag):
    def __init__(self, path, line, scope, name="anony", type=""):
        self.super(path, line, name)
        self.scope = Scope(line)
        

