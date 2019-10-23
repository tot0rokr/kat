import vim
import sys
import kat.lib.error as err
from kat.ui.tabpage import *
import kat.ui.render as render

def isUsing():
    return bool(int(vim.vars['KATUsingExplorer']))

def preInitialize():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    vim.command("silent new " + tab.nameexplorer)
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

    number = tab.window_number('explorer')
    if number != -1:
        return

    current = vim.current.window


    vim.command("silent botright 8new " + tab.nameexplorer)
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

    vim.current.window = current

def detach():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    number = tab.window_number('explorer')
    if number == -1:
        return
    
    vim.command("silent " + str(number) + "hide")

def toggle():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    number = tab.window_number('explorer')
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

    number = tab.window_number('explorer')
    if number == -1:
        attach()

    explorer_bufnr = tab.buffer_number('explorer')

    global_tags = tab.global_tags
    if matched_string is None:
        tags = None
    else:
        tags = []
        if matched_string in global_tags['curconfig']:
            tags += global_tags['curconfig'][matched_string]
        if matched_string in global_tags['preprocess']:
            tags += global_tags['preprocess'][matched_string]

    explorer_buf = vim.buffers[explorer_bufnr]

    explorer_buf.options['readonly'] = False
    explorer_buf.options['modifiable'] = True
    tab.matched_explorer = {} # matched explorer tags
    explorer_buf[:] = None
    explorer_buf.append(render.explorer_show_tags(tab, tags, matched_string))
    explorer_buf[0] = None

    explorer_buf.options['readonly'] = True
    explorer_buf.options['modifiable'] = False
            

def goto_tag(num_line):
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    if len(tab.matched_explorer) == 0:
        return
    elif len(tab.matched_explorer) == 1:
        tag = tab.matched_explorer[0] # only one
    else:
        if num_line not in tab.matched_explorer:
            return
        tag = tab.matched_explorer[num_line]

    name = vim.vars['KATRootDir'].decode() + '/' + str(tag.path)

    vim.command("badd " + name)

    vim.current.window = tab.findSuitableWindowOfNewFile(name) # window is changed
    vim.command("buffer " + name)

    vim.command("call cursor(" + str(tag.line) + ", 1)")

def select_tag(num_line):
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    if num_line not in tab.matched_explorer:
        return
    tags = [tab.matched_explorer[num_line]]

    buf = vim.current.buffer

    vim.command("silent setl noreadonly")
    vim.command("silent setl modifiable")
    tab.matched_explorer = {} # matched explorer tags
    buf[:] = None
    buf.append(render.explorer_show_tags(tab, tags, tags[0].name))
    buf[0] = None

    vim.command("silent setl readonly")
    vim.command("silent setl nomodifiable")
            
    

