import os.path
import time
class File:
    def __init__(self, file):
        self.path = file            # str()
        self.information = "None"
        self.scope = None
        self.type = None            # "std": standard library
                                    # "usr": user definition
        self.defined_tags = set()    # str()
        self.include_files = set()
        self.__last_modified = self.get_modified_time()

    def __call__(self):
        return self.path

    def check_time(self):
        return self.__last_modified == self.get_modified_time()

    def get_modified_time(self):
        return time.ctime(os.path.getmtime(self.path))

    def append_defined_tag(self, name):
        self.defined_tags.add(name)
        return 
        
