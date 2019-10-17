import vim
import sys
import kat.lib.error as err
from kat.ui.tabpage import *
import kat.ui.render as render
import re

def isUsing():
    return bool(int(vim.vars['KATUsingExplorer']))

def preInitialize():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent new " + nameExplorer)
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

    number = explorer_window_number()
    if number != -1:
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent botright 8new " + nameExplorer)
    buf = vim.current.buffer
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

    number = explorer_window_number()
    if number == -1:
        return
    
    vim.command("silent " + str(number) + "hide")

def toggle():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    number = explorer_window_number()
    if number == -1:
        attach()
    else:
        detach()
    

def show_tag(numLine):
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    buf = vim.current.buffer
    matched_string = get_tag_under_cursor(buf)

    number = explorer_window_number()
    if number == -1:
        attach()
    else:
        vim.current.window = tab.tabpage.windows[number - 1]

    buf = vim.current.buffer

    vim.command("silent setl noreadonly")
    vim.command("silent setl modifiable")
    tab.matched_explorer = {} # matched explorer tags
    buf[:] = None
    buf.append(render.explorer_show_tags(tab, matched_string))
    buf[0] = None

    vim.command("silent setl readonly")
    vim.command("silent setl nomodifiable")
            
def explorer_window_number():
    tmp = int(vim.eval("bufwinnr(\"" + nameExplorer + "\")"))
    return tmp

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
    
