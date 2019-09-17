class File:
    def __init__(self, file):
        self.path = file            # str()
        self.information = "None"

    def __call__(self):
        return self.path
