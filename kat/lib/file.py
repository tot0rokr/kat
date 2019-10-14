import os.path
import time
class File:
    def __init__(self, file, rootdir):
        self.path = file            # str()
        self.information = "None"
        self.scope = None
        self.type = None            # "std": standard library
                                    # "usr": user definition
        self.defined_tags = set()    # str()
        self.include_files = set()
        self.__last_modified = self.get_modified_time(rootdir)

    def __call__(self):
        return self.path

    def __str__(self):
        return self.path

    def check_time(self):
        return self.__last_modified == self.get_modified_time()

    def get_modified_time(self, rootdir):
        return time.ctime(os.path.getmtime(rootdir + self.path))

    def append_defined_tag(self, name):
        self.defined_tags.add(name)
        return 
        
