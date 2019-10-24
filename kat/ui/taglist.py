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

    vim.command("silent new " + tab.nametaglist)
    buf = vim.current.buffer
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

    number = tab.window_number('taglist')
    if number != -1:
        return

    current = vim.current.window

    vim.command("exec \'silent botright vert \' . g:KATSizeTagList . \'new " + tab.nametaglist + "\'")
    vim.command("silent setl winfixwidth")
    vim.command("silent setl noswapfile")
    vim.command("silent setl buftype=nofile")
    vim.command("silent setl nomodifiable")
    vim.command("silent setl nobuflisted")
    vim.command("silent setl readonly")
    vim.command("silent setg winfixwidth&")
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
    
    number = tab.window_number('taglist')
    if number == -1:
        return
    
    vim.command("silent " + str(number) + "hide")

def toggle():
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]
    
    number = tab.window_number('taglist')
    if number == -1:
        attach()
    else:
        detach()
    
def goto_tag(num_line):
    if not isUsing():
        return

    tab = tabpages[currentTabpageNumber()]

    buff = tab.shown_taglist_buff
    if buff is None:
        return

    if num_line not in buff.matched_taglist:
        return
    tag = buff.matched_taglist[num_line]

    name = vim.vars['KATRootDir'].decode() + '/' + str(tag.path)

    number = tab.window_number(buff.buf.name)
    if number == -1:
        return
    vim.current.window = vim.windows[number - 1]

    vim.current.window.cursor = (tag.line, 0)

def make_taglist_buf(buf, name):
    render.taglist(buf, name)

def show_taglist_buf():
    if not isUsing():
        return
    if vim.vars['CompletedLoad'] == 0:
        return

    tab = tabpages[currentTabpageNumber()]

    buf = vim.current.buffer
    if buf.name not in buffers:
        return
    buff = buffers[buf.name]
    make_taglist_buf(buff, buf.name)

    taglist_winnr = tab.window_number('taglist')
    if taglist_winnr == -1:
        return

    taglist_bufnr = tab.buffer_number('taglist')

    taglist_buf = vim.buffers[taglist_bufnr]
    taglist_buf.options['readonly'] = False
    taglist_buf.options['modifiable'] = True

    taglist_buf[:] = None
    taglist_buf.append(buff.buf_taglist)
    taglist_buf[0] = None

    taglist_buf.options['readonly'] = True
    taglist_buf.options['modifiable'] = False

    tab.shown_taglist_buff = buff

    #  load_state()

#  def load_state():
    #  if not isUsing():
        #  return
    #  if vim.vars['CompletedLoad'] == 0:
        #  return

    #  tab = tabpages[currentTabpageNumber()]

    #  buf = vim.current.buffer
    #  if buf.name not in buffers:
        #  return
    #  buff = buffers[buf.name]

    #  number = tab.window_number('taglist')
    #  if number == -1:
        #  return
    #  taglist_win = tab.tabpage.windows[number - 1]

    #  taglist_win.cursor = buff.taglist_cursor

    #  taglist_win.vars['target'] = buf.name
    #  print("load" + str(buff.taglist_cursor))

#  def store_state():
    #  if not isUsing():
        #  return
    #  if vim.vars['CompletedLoad'] == 0:
        #  return

    #  tab = tabpages[currentTabpageNumber()]

    #  number = tab.window_number('taglist')
    #  if number == -1:
        #  print("storeerror tag " + str(taglist_win.cursor))
        #  return
    #  taglist_win = tab.tabpage.windows[number - 1]

    #  bufname = taglist_win.vars['target']

    #  if bufname not in buffers:
        #  print("storeerror" + str(taglist_win.cursor))
        #  return
    #  buff = buffers[bufname]

    #  buff.taglist_cursor = taglist_win.cursor
    #  print("store" + str(taglist_win.cursor))

