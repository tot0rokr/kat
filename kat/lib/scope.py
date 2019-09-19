from file       import File
class Scope:
    def __init__(self, path, scope, start=None, end=None):
        self.path = path            # File()
        self.line = [start, end]    # [Int, Int]
                                    # [0, 0] is all scope in file
        self.information = "None"
        self.container = scope

    def __call__(self):
        return {path:self.path(), start:self.line[0], end:self.line[1]}
