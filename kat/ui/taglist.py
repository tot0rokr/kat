import vim
import sys
import kat.lib.error as err
from kat.ui.tabpage import *
import kat.ui.render as render

def isUsing():
    return bool(int(vim.vars['KATUsingTagList']))

def preInitialize():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent new " + nameTagList)
    render.taglist(tab, vim.current.buffer)
    vim.command("silent set noswapfile")
    vim.command("silent set buftype=nofile")
    vim.command("silent set buftype=nowrite")
    vim.command("silent set nomodifiable")
    vim.command("silent set nobuflisted")
    vim.command("hide")


def attach():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent botright vert 30new " + nameTagList)
    vim.command("silent set buftype=nofile")
    vim.command("silent set buftype=nowrite")
    vim.command("silent set nomodifiable")
    vim.command("silent set nobuflisted")



def detach(number):
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    vim.command("silent " + str(number) + "hide")
    #  try:
        #  vim.command("silent " + str(number) + "hide")
    #  except:
        #  err.error("Vim:E444: Can't close as this window is last one")

def toggle():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    #  w = tab.findFileTreeWindow()
    
    number = taglistWindowNumber()

    if number == -1:
        attach()
    else:
        detach(number)
    

def taglistWindowNumber():
    tmp = int(vim.eval("bufwinnr(\"" + nameTagList + "\")"))
    return tmp
    



