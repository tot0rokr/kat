import vim
import kat.ui.render
from kat.katconfig import Katconfig

nameFileTree = vim.eval("g:KATBufNameFileTree")
nameTagList = vim.eval("g:KATBufNameTagList")

def currentTabpageNumber():
    return vim.eval('tabpagenr()')

def currentWindow():
    return vim.current.buffer

tabpages = {}
class TabPage:
    def __init__(self, katconfig):
        self.tabpageNumber = currentTabpageNumber()
        self.tabpage = vim.current.tabpage
        self.katconfig = katconfig
        self.buf = []       # buf contents
        self.matched = {} # match between files and filetree
        self.helplen = 0
        tabpages[self.tabpageNumber] = self




