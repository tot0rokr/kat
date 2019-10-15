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

import codecs

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
    
    i = 0
    files_nr = len(katconfig['files'])
    for it in katconfig['files']:
        i += 1
        print(str(i) + "/" + str(files_nr) + " - " + it.path)
        f = open(kernel_root_dir + '/' + it.path, "r")
        try:
            raw_data = f.read()
        except UnicodeDecodeError:
            f = codecs.open(kernel_root_dir + '/' + it.path, "r", 'utf-8')

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


