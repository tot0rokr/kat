import vim
import kat.ui.render
from kat.katconfig import Katconfig

nameFileTree = vim.eval("g:KATBufNameFileTree")
nameTagList = vim.eval("g:KATBufNameTagList")
nameExplorer = vim.eval("g:KATBufNameExplorer")

def currentTabpageNumber():
    return vim.eval('tabpagenr()')

def currentWindow():
    return vim.current.buffer

tabpages = {}
class TabPage:
    def __init__(self, katconfig, global_tags):
        self.tabpageNumber = currentTabpageNumber()
        self.tabpage = vim.current.tabpage
        self.katconfig = katconfig
        self.buf_filetree = []       # buf contents
        self.buf_taglist = []       # buf contents
        self.buf_explorer = []       # buf contents
        self.global_tags = global_tags
        self.matched = {} # match between files and filetree
        self.matched_explorer = {}  # if multiple tags are matched this is made.
                                    # otherwise, this is empty.
        self.helplen = 0
        tabpages[self.tabpageNumber] = self




