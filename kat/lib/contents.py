from scope      import Scope
class Contents:
    def __init__(self):
        self.validScope = None      # Scope()
        self.text = None            # 
        self.type = None

    def __call__(self):
        return self.text

