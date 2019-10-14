from kat.lib.file       import File
class Scope:
    def __init__(self, path, scope, start=None, end=None):
        self.path = path            # File()
        self.line = [start, end]    # [Int, Int]
                                    # [0, 0] is all scope in file
        self.information = "None"
        if scope is None:
            self.contained_by = self
        else:
            self.contained_by = scope
        self.include = []

    def __call__(self):
        return {path:self.path(), start:self.line[0], end:self.line[1]}

    def __str__(self):
        return str((self.path.path, self.line, "by_" + str(self.contained_by.line)))

    #  def set_start(self, start):
        #  self.line[0] = start

    #  def set_end(self, end):
        #  self.line[1] = end

class PreprocessScope(Scope):
    def __init__(self, path, scope, start=None, end=None):
        super().__init__(path, scope, start, end)       
        self.pre_associator = None
        self.post_associator = None
        self.condition = []         # expression parsing tree

    def __str__(self):
        line1 = None
        line2 = None
        if self.pre_associator is not None:
            line1 = self.pre_associator.line
        if self.post_associator is not None:
            line2 = self.post_associator.line
        return str((super().__str__(), "pre_" + str(line1), "post_" + str(line2)))
        #  return str((super().__str__(), self.pre_associator.line, self.post_associator.line))

