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
    buf = vim.current.buffer
    render.taglist(tab)
    buf.append(tab.buf_taglist)
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

    number = window_number('taglist')
    if number != -1:
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent botright vert 30new " + nameTagList)
    buf = vim.current.buffer
    if len(buf) == 1:
        vim.command("silent setl noreadonly")
        vim.command("silent setl modifiable")
        buf.append(tab.buf_taglist)
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



def detach():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    number = window_number('taglist')
    if number == -1:
        return
    
    vim.command("silent " + str(number) + "hide")

def toggle():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    number = window_number('taglist')
    if number == -1:
        attach()
    else:
        detach()
    



