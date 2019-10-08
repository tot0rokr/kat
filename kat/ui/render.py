import vim
import kat.katconfig as kc
from kat.ui.tabpage import *

prefixComment = lambda x: "\" " + x


def taglist(tab, buf):
    pass

def makeFileTree(filelist):
    filestack = []
    contents = []

    for it in filelist:                     # iterate with files
        path = it.path.split("/")

        i = 0
        while i < len(path) - 1:          # check file path
            if i >= len(filestack):
                break
            elif path[i] != filestack[i]:
                filestack = filestack[:i]
                break
            i += 1

        if len(path) - 1 > len(filestack):  # other dir from upper file
            for it in path[i:-1]:
                filestack.append(it)
                contents.append({'depth': len(filestack) - 1,
                            'name': it,
                            'type': 'd'})

        contents.append({'depth': len(filestack),
                    'name': path[-1],
                    'type': 'f'})

    return contents

def filetree(tab, buf):
    del buf[:]
    
    comments = []
    ftcomments = []
    kcomments = []

    comments.append("Press ?, for help")
    comments.append("j: next line")
    comments.append("k: prev line")
    comments.append("<Space>: next line")
    comments.append("<Enter>: open file or expand directory or fold directory")
    comments.append("q: close tab")
    comments = list(map(prefixComment, comments))
    buf.append(comments)

    ftcomments.append("=File Tree=")
    ftcomments.append("")
    ftcomments = list(map(prefixComment, ftcomments))
    buf.append(ftcomments)

    contents = makeFileTree(tab.katconfig['files'])

    for it in contents:
        line = "  " * it['depth'] \
              + ("▼ " if it['type'] == 'd' else "  ") \
              + it['name']
        buf.append(line)


    kcomments.append("=Kconfig=")
    kcomments.append("")
    kcomments = list(map(prefixComment, kcomments))
    buf.append(kcomments)

    contents = makeFileTree(tab.katconfig['kconfigs'])

    for it in contents:
        line = "  " * it['depth'] \
              + ("▼ " if it['type'] == 'd' else "  ") \
              + it['name']
        buf.append(line)

