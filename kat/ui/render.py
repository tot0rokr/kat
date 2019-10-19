import vim
import kat.katconfig as kc
from kat.ui.tabpage import *

prefixComment = lambda x: "# " + x
prefixHelp = lambda x: "\" " + x

def explorer_show_tags(tab, tags, string):
    buf = []
    global_tags = tab.global_tags

    rootdir = vim.vars['KATRootDir'].decode() + '/'
    title = "=          KAT-Explorer          ="
    buf.append(title)

    if tags is None:
        # TODO: string is not tag
        buf.append("!!!!!  TAG NOT TAKEN  !!!!!")
    elif len(tags) == 0:
        # TODO: can't find any tag
        buf.append("!!!!! > " + string + " < TAG NOT FOUND !!!!!")
    elif len(tags) == 1:
        tag = tags[0]
        path = tag.path
        line = tag.line - 1
        # TODO: The height is height of explorer's window minus one
        height = 7
        start = tag.line - (height // 2) - 1
        with open(rootdir + path, 'r') as f:
            readlines = f.readlines()[start:start + height]
        buf += readlines
        tab.matched_explorer[0] = tag
    else:
        padding_nr = len(title) - 6 - len(string)
        buf.pop()
        buf.append("=" + " " * (padding_nr // 2) + "> "
                + string + " <" + " " * (padding_nr - padding_nr // 2) + "=")
        for it in tags:
            path = it.path
            line = it.line - 1
            with open(rootdir + path, 'r') as f:
                buf.append(path + "|" + str(line) + "| " \
                        + f.readlines()[line])
                tab.matched_explorer[len(buf)] = it

    return buf

def taglist(agent, name):
    rootdir = vim.vars['KATRootDir'].decode() + '/'
    contents = []
    contents.append(rootdir)
    contents.append(name.replace(rootdir, ''))
    contents.append("")
    contents.append("# =TagList=")
    contents.append("")

    #  buf = ["asdasd", "asddasd"]
    for it in agent.local_tags:
        contents.append(it.name)
        agent.matched_taglist[len(contents)] = it

    #  buf += contents
    #  for it in contents:
        #  line = "  " * it['depth']
        #  if it['type'] == 'd':
            #  line += "▼ "
        #  elif it['type'] == 'f':
            #  line += "- "
            #  tab.matched_filetree[len(buf) + 1] = it['path']
        #  line += it['name']
        #  buf.append(line)
    agent.buf_taglist = contents
    #  return buf

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
                break
            i += 1

        filestack = filestack[:i]

        if len(path) - 1 > len(filestack):  # other dir from upper file
            for it2 in path[i:-1]:
                filestack.append(it2)
                contents.append({'depth': len(filestack) - 1,
                            'name': it2,
                            'type': 'd'})

        contents.append({'depth': len(filestack),
                    'name': path[-1],
                    'type': 'f',
                    'path': it})

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

    contents = makeFileTree(tab.katconfig['files'])

    for it in contents:
        line = "  " * it['depth']
        if it['type'] == 'd':
            line += "▼ "
        elif it['type'] == 'f':
            line += "- "
            tab.matched_filetree[len(buf) + 1] = it['path']
        line += it['name']
        buf.append(line)


    kcomments.append("=Kconfig=")
    kcomments.append("")
    kcomments = list(map(prefixComment, kcomments))
    buf += kcomments

    contents = makeFileTree(tab.katconfig['kconfigs'])
    for it in contents:
        line = "  " * it['depth']
        if it['type'] == 'd':
            line += "▼ "
        elif it['type'] == 'f':
            line += "- "
            tab.matched_filetree[len(buf) + 1] = it['path']
        line += it['name']
        buf.append(line)

    tab.buf_filetree = buf
    return buf

