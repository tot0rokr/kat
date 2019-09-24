class File:
    def __init__(self, file):
        self.path = file            # str()
        self.information = "None"
        self.scope = None
        #  self.type = None            # "std": standard library
                                    # "usr": user definition
        self.callerList = []

    def __call__(self):
        return self.path
