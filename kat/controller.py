from kat.lib.tag import Tag
from kat.lib.file import File
from kat.lib.scope import Scope
from kat.tracer import ccscanner as ccs
from kat.tracer import ccparser as ccp
from kat.tracer import ppscanner as pps
from kat.tracer import ppparser as ppp
from kat.ui.tabpage import *
import kat.ui.filetree as ft
import kat.ui.taglist as tl
from kat.katconfig import Katconfig

import vim

def initializeKAT(configPath):
    config = Katconfig(configPath)
    kernel_root_dir = vim.vars['KATRootDir'].decode()

    katconfig = {}

    cc_tags = []
    pp_tags = []

    files = []
    for it in config.files:
        files.append(File(it, kernel_root_dir + '/'))
    #  files = sorted(files, key=lambda x: x.path)
    katconfig['files'] = files
    
    for it in katconfig['files']:
        f = open(kernel_root_dir + '/' + it.path, "r")
        raw_data = f.read()
        f.close()
        tokens = pps.scan(raw_data)
        it.scope = Scope(it.path, None, 0, 0)
        tags, _, _ = ppp.parse(tokens, it)
        pp_tags += tags

    print("files load success")

    kconfigs = []
    for it in config.kconfigs:
        kconfigs.append(File(it, vim.vars['KATRootDir'].decode() + '/'))
    #  kconfigs = sorted(kconfigs, key=lambda x: x.path)
    katconfig['kconfigs'] = kconfigs

    print("kconfigs load success")

    TabPage(katconfig)
    ft.preInitialize()
    tl.preInitialize(pp_tags)


