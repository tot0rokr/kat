from file       import File
class Scope:
    def __init__(self):
        self.path = None            # File()
        self.line = [None, None]    # [Int, Int]
        self.information = "None"

    def __call__(self):
        return {path:self.path(), start:self.line[0], end:self.line[1]}
