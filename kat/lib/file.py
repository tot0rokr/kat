import os.path
import time
class File:
    def __init__(self, file):
        self.path = file            # str()
        self.information = "None"
        self.scope = None
        self.type = None            # "std": standard library
                                    # "usr": user definition
        self.definedTags = set()    # str()
        self.lastModified = self.getModifiedTime()

    def __call__(self):
        return self.path


    def getModifiedTime(self):
        return time.ctime(os.path.getmtime(self.path))

    def appendDefinedTag(self, name):
        self.definedTags.add(name)
        return 
        
