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
    render.filetree(tab)
    buf.append(tab.buf_filetree)
    buf[0] = None
    vim.command("silent setl buftype=nofile")
    vim.command("silent setl nomodifiable")
    vim.command("silent setl nobuflisted")
    vim.command("silent setg buftype&")
    vim.command("silent setg modifiable&")
    vim.command("silent setg buflisted&")
    vim.command("hide")
    

def attach():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent topleft vert 30new " + nameFileTree)
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

    # fold option
    #  vim.command("silent setl foldmethod=indent")
    #  defaultsw = vim.eval("&shiftwidth")
    #  vim.command("silent setl shiftwidth=2")


    #  vim.command("silent setg foldmethod&")
    #  vim.command("silent setg shiftwidth=" + defaultsw)




def detach():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    number = filetree_window_number()
    if number == -1:
        return
    
    vim.command("silent " + str(number) + "hide")

def toggle():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    number = filetree_window_number()
    if number == -1:
        attach()
    else:
        detach()
    

def openFile(numLine):
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    if numLine not in tab.matched:
        return

    name = vim.vars['KATRootDir'].decode() + '/' + tab.matched[numLine].path
    vim.command("badd " + name)

    vim.current.window = findSuitableWindowOfNewFile(tab) # window is changed
    vim.command("buffer " + name)
    
            
def filetree_window_number():
    tmp = int(vim.eval("bufwinnr(\"" + nameFileTree + "\")"))
    return tmp

def findSuitableWindowOfNewFile(tab):
    #  if vim.eval("bufname(" \
        #  + str(int(vim.eval("winbufnr(" + str(win.number) + ")"))) \
        #  + ")").decode() == nameFileTree:
    backupWindow = vim.current.window
    window = None
    for w in tab.tabpage.windows:
        if w.buffer.name.split("/")[-1] != nameFileTree:
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
    vim.current.window = backupWindow
    return window
    

