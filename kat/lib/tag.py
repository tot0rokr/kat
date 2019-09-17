from contents   import Contents
from file       import File
class Tag:
    def __init__(self, path, line, name, type=None, defi=None):
        self.path = path               # File() / file path
        self.line = line               # Int    / line number
        self.name = name                 # str()  / tag name
        self.contents = Contents()     # Contents
        self.type = type                 # what it is used type in code
        self.definition = defi             # DefinitionTag()  / definition tag



class DefinitionTag(Tag):
    def __init__(self, path, line, name, scope, type=None):
        self.super(path, line, name, type, self)
        self.scope = scope                   # ScopeTag() / valid scope. 


class ScopeTag(Tag):
    def __init__(self):
        self.super()
        self.scope = None
        

