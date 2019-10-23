import vim
import sys
import kat.lib.error as err
from kat.ui.tabpage import *
import kat.ui.render as render

def isUsing():
    return bool(int(vim.vars['KATUsingFileTree']))

def preInitialize():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent new " + tab.namefiletree)
    buf = vim.current.buffer
    render.filetree(tab)
    buf.append(tab.buf_filetree)
    buf[0] = None
    vim.command("silent setl noswapfile")
    vim.command("silent setl buftype=nofile")
    vim.command("silent setl nomodifiable")
    vim.command("silent setl nobuflisted")
    vim.command("silent setl readonly")
    vim.command("silent setg swapfile&")
    vim.command("silent setg buftype&")
    vim.command("silent setg modifiable&")
    vim.command("silent setg buflisted&")
    vim.command("silent setg readonly&")
    vim.command("hide")
    

def attach():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    number = tab.window_number('filetree')
    if number != -1:
        return

    current = vim.current.window

    vim.command("silent topleft vert 30new " + tab.namefiletree)
    buf = vim.current.buffer
    if len(buf) == 1:
        vim.command("silent setl noreadonly")
        vim.command("silent setl modifiable")
        buf.append(tab.buf_filetree)
        buf[0] = None
        detach()
        attach()
        return
    vim.command("silent setl noswapfile")
    vim.command("silent setl buftype=nofile")
    vim.command("silent setl nomodifiable")
    vim.command("silent setl nobuflisted")
    vim.command("silent setl readonly")
    vim.command("silent setg swapfile&")
    vim.command("silent setg buftype&")
    vim.command("silent setg modifiable&")
    vim.command("silent setg buflisted&")
    vim.command("silent setg readonly&")

    vim.current.window = current

def detach():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    number = tab.window_number('filetree')
    if number == -1:
        return
    
    vim.command("silent " + str(number) + "hide")

def toggle():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    number = tab.window_number('filetree')
    if number == -1:
        attach()
    else:
        detach()
    

def openFile(numLine):
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    if numLine not in tab.matched_filetree:
        return

    name = vim.vars['KATRootDir'].decode() + '/' + tab.matched_filetree[numLine].path
    vim.command("badd " + name)

    vim.current.window = tab.findSuitableWindowOfNewFile() # window is changed
    vim.command("buffer " + name)
    
            
