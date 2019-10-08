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

    vim.command("silent new " + nameFileTree)
    buf = vim.current.buffer
    vim.command("silent setl filetype=" + vim.vars['KATFiletypeFileTree'].decode())
    #  buf.options['filetype'] = vim.vars['KATFiletypeFileTree'].decode()
    render.filetree(tab, buf)
    #  buf.options['swapfile'] = False
    #  buf.options['buftype'] = b'nofile'
    #  buf.options['modifiable'] = False
    #  buf.options['buflisted'] = False
    vim.command("silent setl noswapfile")
    vim.command("silent setl buftype=nofile")
    vim.command("silent setl nomodifiable")
    vim.command("silent setl nobuflisted")
    vim.command("silent setl readonly")
    vim.command("silent setg swapfile&")
    vim.command("silent setg buftype&")
    vim.command("silent setg modifiable&")
    vim.command("silent setg buflisted&")
    vim.command("silent setg noreadonly")
    vim.command("hide")
    

def attach():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent topleft vert 30new " + nameFileTree)
    buf = vim.current.buffer
    if len(buf) == 1:
        vim.command("silent setg noreadonly")
        vim.command("silent setl modifiable")
        preInitialize()
    vim.command("silent setl noswapfile")
    vim.command("silent setl buftype=nofile")
    vim.command("silent setl nomodifiable")
    vim.command("silent setl nobuflisted")
    vim.command("silent setg readonly")
    vim.command("silent setg swapfile&")
    vim.command("silent setg buftype&")
    vim.command("silent setg modifiable&")
    vim.command("silent setg buflisted&")
    vim.command("silent setg readonly&")



def detach(number):
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    vim.command("silent " + str(number) + "hide")

def toggle():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    number = tab.filetreeWindowNumber()

    if number == -1:
        attach()
    else:
        detach(number)
    
