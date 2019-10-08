import kat.lib.error as err

class Katconfig:
    def __init__(self, configPath):
        self.path = configPath

        f = open(self.path, "r")

        data = f.read()
        data = data.split(":")
        if "options" in data:
        #  if ":options:" in lines:
            #  indexOptions = lines.index("options")
            indexOptions = data.index("options")
        else:
            err.error("Not found options")
        if "files" in data:
        #  if ":files:" in lines:
            #  indexFiles = lines.index("files")
            indexFiles = data.index("files")
        else:
            err.error("Not found files")
        if "kconfigs" in data:
        #  if ":kconfigs:" in lines:
            #  indexKconfigs = lines.index("kconfigs")
            indexKconfigs = data.index("kconfigs")
        else:
            err.error("Not found kconfigs")
        
        self.options = data[indexOptions + 1].split("\n")
        self.files = data[indexFiles + 1].split("\n")
        self.kconfigs = data[indexKconfigs + 1].split("\n")
        self.options.remove("")
        self.files.remove("")
        self.kconfigs.remove("")
        #  options = lines[indexOptions + 1:indexFiles]
        #  files = lines[indexFiles + 1:indexKconfigs]
        #  kconfigs = lines[indexKconfigs + 1:]

        f.close()
