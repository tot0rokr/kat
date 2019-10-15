import vim
import kat.katconfig as kc
from kat.ui.tabpage import *

prefixComment = lambda x: "# " + x
prefixHelp = lambda x: "\" " + x


def taglist(tab):
    buf = []
    contents = []
    for it in tab.global_tags:
        contents.append(it.name)

    buf += contents
    tab.buf_taglist = buf
    return buf

def makeFileTree(filelist):
    filestack = []
    contents = []
    #  matched = {}

    for it in filelist:                     # iterate with files
        path = it.path.split("/")

        i = 0
        while i < len(path) - 1:          # check file path
            if i >= len(filestack):
                break
            elif path[i] != filestack[i]:
                break
            i += 1

        filestack = filestack[:i]

        if len(path) - 1 > len(filestack):  # other dir from upper file
            for it2 in path[i:-1]:
                filestack.append(it2)
                contents.append({'depth': len(filestack) - 1,
                            'name': it2,
                            'type': 'd'})

        #  matched[len(contents)] = it
        contents.append({'depth': len(filestack),
                    'name': path[-1],
                    'type': 'f',
                    'path': it})

    #  return contents, matched
    return contents

def filetree(tab):
    buf = []
    
    comments = []   # help comment 
    fcomments = []  # file comment
    kcomments = []  # kconfig comment

    comments.append("Press ?, for help")
    comments.append("Press ? again, if you")
    comments.append("want to close |help|")
    comments.append("")
    comments.append("= terminate =")
    comments.append("<kat-prefix>f: toggle")
    comments.append("q: quit")
    comments.append("")
    comments.append("= file =")
    comments.append("<Enter>: file open")
    comments.append("")
    comments.append("= folding =")
    comments.append("c: close dir")
    comments.append("C: recursively close dir")
    comments.append("o: open dir")
    comments.append("O: recursively open dir")
    comments.append("")
    comments.append("r: reduce a level of dir")
    comments.append("R: recursively reduce max")
    comments.append("   level of dir")
    comments.append("p: expand a level of dir")
    comments.append("P: recursively expand max")
    comments.append("   level of dir")
    comments.append("")
    comments.append("a: toggle open/close")
    comments.append("<space>: toggle open/close")
    comments.append("         as \'a\'")
    comments.append("A: recursively toggle")
    comments.append("   open/close")
    comments.append("")
    comments.append("= movement =")
    comments.append("j: next line")
    comments.append("k: prev line")
    comments.append("J: last line of current")
    comments.append("   opened dir")
    comments.append("K: top line of current")
    comments.append("   opened dir")
    comments.append("L: next dir")
    comments.append("H: prev dir")
    comments.append("")
    comments = list(map(prefixHelp, comments))
    buf += comments

    buf.append(vim.vars['KATRootDir'].decode())
    fcomments.append("=File Tree=")
    fcomments.append("")
    fcomments = list(map(prefixComment, fcomments))
    buf += fcomments
    #  buf.append(fcomments)

    contents = makeFileTree(tab.katconfig['files'])
    #  tab.matched['files'] = matched

    for it in contents:
        line = "  " * it['depth']
        if it['type'] == 'd':
            line += "▼ "
        elif it['type'] == 'f':
            line += "- "
            tab.matched[len(buf) + 1] = it['path']
        line += it['name']
        #  line = "  " * it['depth'] \
              #  + ("▼ " if it['type'] == 'd' else "- ") \
              #  + it['name']
        buf.append(line)


    kcomments.append("=Kconfig=")
    kcomments.append("")
    kcomments = list(map(prefixComment, kcomments))
    buf += kcomments
    #  buf.append(kcomments)

    contents = makeFileTree(tab.katconfig['kconfigs'])
    #  contents, matched = makeFileTree(tab.katconfig['kconfigs'])
    #  tab.matched['kconfigs'] = matched

        #  line = "  " * it['depth'] \
              #  + ("▼ " if it['type'] == 'd' else "- ") \
              #  + it['name']
    for it in contents:
        line = "  " * it['depth']
        if it['type'] == 'd':
            line += "▼ "
        elif it['type'] == 'f':
            line += "- "
            tab.matched[len(buf) + 1] = it['path']
        line += it['name']
        #  line = "  " * it['depth'] \
              #  + ("▼ " if it['type'] == 'd' else "- ") \
              #  + it['name']
        buf.append(line)

    tab.buf_filetree = buf
    return buf

