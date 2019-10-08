from kat.lib.tag import Tag
from kat.lib.file import File
from kat.tracer import curconfigscanner as ccs
from kat.tracer import curconfigparser as ccp
from kat.ui.tabpage import *
import kat.ui.filetree as ft
import kat.ui.taglist as tl
from kat.katconfig import Katconfig

def initializeKAT(configPath):
    #  print (configPath)
    #  kc.initConfigFile(configPath)
    config = Katconfig(configPath)

    katconfig = {}
    
    files = []
    for it in config.files:
        files.append(File(it))
    katconfig['files'] = files

    kconfigs = []
    for it in config.kconfigs:
        kconfigs.append(File(it))
    katconfig['kconfigs'] = kconfigs

    TabPage(katconfig)
    ft.preInitialize()
    tl.preInitialize()


