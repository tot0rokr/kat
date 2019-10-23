import vim
import kat.ui.render
from kat.katconfig import Katconfig
import re

nameFileTree = vim.eval("g:KATBufNameFileTree")
nameTagList = vim.eval("g:KATBufNameTagList")
nameExplorer = vim.eval("g:KATBufNameExplorer")

def currentTabpageNumber():
    return vim.current.tabpage.vars['tabid']
    #  return vim.eval('tabpagenr()')

tabpages = {}       # global tabpages. 
buffers = {}        # global buffers.
class TabPage: # This must be initialized by controller when VimEnter or
               # TabNew events occurred.
    nr = 0
    def __init__(self, katconfig, global_tags):
        TabPage.nr += 1
        self.tabpageNumber = TabPage.nr
        self.tabpage = vim.current.tabpage
        self.katconfig = katconfig
        self.buf_filetree = []      # buf contents
        self.buf_explorer = []      # buf contents
        self.shown_taglist_buff = None
        self.global_tags = global_tags
        self.matched_filetree = {}  # what is matched between files and filetree
        self.matched_explorer = {}  # if multiple tags are matched this is made.
                                    # otherwise, this is empty.
        self.namefiletree = nameFileTree + str(TabPage.nr)
        self.nametaglist = nameTagList + str(TabPage.nr)
        self.nameexplorer = nameExplorer + str(TabPage.nr)
        self.helplen = 0
        tabpages[self.tabpageNumber] = self

    def window_number(self, kind):
        tmp = None
        if kind == 'filetree':
            tmp = int(vim.eval("bufwinnr(\"" + self.namefiletree + "\")"))
        elif kind == 'taglist':
            tmp = int(vim.eval("bufwinnr(\"" + self.nametaglist + "\")"))
        elif kind == 'explorer':
            tmp = int(vim.eval("bufwinnr(\"" + self.nameexplorer + "\")"))
        else:
            tmp = int(vim.eval("bufwinnr(\"" + kind + "\")"))
        return tmp

    def buffer_number(self, kind):
        tmp = None
        if kind == 'filetree':
            tmp = int(vim.eval("bufnr(\"" + self.namefiletree + "\")"))
        elif kind == 'taglist':
            tmp = int(vim.eval("bufnr(\"" + self.nametaglist + "\")"))
        elif kind == 'explorer':
            tmp = int(vim.eval("bufnr(\"" + self.nameexplorer + "\")"))
        else:
            tmp = int(vim.eval("bufnr(\"" + kind + "\")"))
        return tmp



    def findSuitableWindowOfNewFile(self, filename):
        tab = self
        current = vim.current.window
        window = None
        number = tab.window_number(filename)
        if number != -1:
            return tab.tabpage.windows[number - 1]
        for w in tab.tabpage.windows:
            filename = w.buffer.name.split("/")[-1]
            if filename != self.namefiletree \
                    and filename != self.nametaglist \
                    and filename != self.nameexplorer:
                bufinfo = vim.eval("getbufinfo(winbufnr(" + str(w.number) \
                            + "))[0]")
                if bool(int(bufinfo['hidden'])) is True:
                    continue
                if bool(int(bufinfo['listed'])) is False:
                    continue
                if bool(int(bufinfo['loaded'])) is False:
                    continue
                if window is None:
                    window = w
                if bool(int(bufinfo['changed'])) is False:
                    window = w
                    return window
        if window is not None:
            vim.current.window = window
        vim.command("silent bo vert new")
        window = vim.current.window
        vim.current.window = current
        return window

class Buffer:
    def __init__(self, buf, tags): # vim.buffer
        self.buf = buf
        self.buf_taglist = []
        self.local_tags = tags
        self.matched_taglist = {}
        #  self.cursor = {} # it is made each tabpage
        #  self.taglist_cursor = (1, 0)



def get_tag_under_cursor(buf):
    curpos = vim.eval("getcurpos()")
    lnum = int(curpos[1]) - 1
    col = int(curpos[2]) - 1

    line = buf[lnum]
    word = re.compile(r"((struct|enum|union)[ \t]+)?[A-Za-z_][A-Za-z0-9_]*")
    pos = 0
    while True:
        matched_string = word.search(line[pos:])
        if matched_string is None:
            return None
        elif matched_string.start() <= col - pos \
                and col - pos < matched_string.end():
            return matched_string.group()
        else:
            pos += matched_string.end()
    
