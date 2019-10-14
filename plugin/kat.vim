" SECTION: script init {{{1
"==============================================================================
" SECTION: check version {{{2
if exists("loaded_kat")
    finish
endif
if v:version < 800
    echoerr "KAT: Error(2): this plugin requires vim version >= 8."
    finish
endif
if !has('python3')
    echoerr "Kat: Error(1): Not be able to use python3"
    echoerr "Required vim compiled with +python3"
    finish
endif
let g:loaded_kat = 1

let g:KATConfigPath = findfile("kat.ref", ".;")

if empty(g:KATConfigPath)
    finish
endif

let s:tmp = substitute(g:KATConfigPath, "/\\=[^/]*$", "", "")
if s:tmp == ""
    let g:KATRootDir = getcwd()
else
    let g:KATRootDir = s:tmp
endif




" Function: s:InitVariable() function {{{2
" This function is used to initialise a given variable to a given value. The
" variable is only initialised if it does not exist prior
" 
" Args:
"   -var: the name of the var to be initialised
"   -value: the value to initialise var to
" 
" Returns:
"   1 if the var is set, 0 otherwise
"
function s:InitVariable(var, value)
    if !exists(a:var)
        execute 'let ' . a:var . ' = ' . "'" . a:value. "'"
        return 1
    endif
    return 0
endfunction

" SECTION: variable initialization {{{2
call s:InitVariable("g:KATUsing", 1)
call s:InitVariable("g:KATUsingFileTree", 1)
call s:InitVariable("g:KATUsingTagList", 1)
call s:InitVariable("g:KATCreateDefaultMappings", 1)
call s:InitVariable("g:KATBufNameFileTree", "=KAT-FileTree=")
call s:InitVariable("g:KATBufNameTagList", "=KAT-TagList=")
call s:InitVariable("g:KATFiletypeFileTree", "katfiletree")
call s:InitVariable("g:KATFiletypeiTagList", "kattaglist")

if !g:KATUsing
    finish
endif



" SECTION: load python {{{2
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..'))
sys.path.insert(0, python_root_dir)
import kat.ui.tabpage as tp
import kat.ui.filetree as ft
import kat.ui.taglist as tl
import kat.ui.render as rd
import kat.controller as ctrl
EOF


" SECTION: auto commands {{{2
"==============================================================================
augroup kat
    " autocmd VimEnter,TabNew *.c,*.h,*.asm :python3 tp.TabPage()
    autocmd VimEnter,TabNew * :python3 ctrl.initializeKAT(vim.eval("g:KATConfigPath"))
augroup END

augroup katfiletree
    " autocmd BufNewFile,BufRead =KAT-FileTree= setf katfiletree
    exec 'autocmd BufEnter ' . g:KATBufNameFileTree
                \ . ' setl filetype=' . g:KATFiletypeFileTree
    " exec 'autocmd FileType '.g:KATFiletypeFileTree
                " \ . ' source ' . s:plugin_root_dir . '/lib/kat/key_map.vim'
                " \ . 'call s:KATKeyMapFileTree()' 
    " exec 'autocmd BufLeave '.g:KATBufNameFileTree
                " \ . ' :python3 print("hello")'
augroup END

augroup kattaglist
    exec 'autocmd BufEnter ' . g:KATBufNameTagList
                \ . ' setl filetype=' . g:KATFiletypeiTagList
augroup END

" augroup kattaglist
    " " exec 'autocmd BufLeave '.g:KATBufNameTagList.' setf kattaglist'
" augroup END


" SECTION: FileTree {{{1
"==============================================================================
" KATFileTree
"

" Function: s:KATAttachFileTree() function {{{2
" This function make the FileTree opened if the FileTree is closed.
" Then if FileTree is closed, it do nothing.
" 
function s:KATAttachFileTree()
    python3 ft.attach()
endfunction


" Function: s:KATDetachFileTree() function {{{2
" This function make the FileTree closed if the FileTree is opened.
" Then if FileTree is opened, it do nothing.
" 
function s:KATDetachFileTree()
    python3 ft.detach()
endfunction

" Function: s:KATToggleFileTree() function {{{2
" This function make the FileTree closed if the FileTree is opened.
" Then if the FileTree is opened, oppositely do.
" 
function s:KATToggleFileTree()
    python3 ft.toggle()
endfunction

" Function: s:KATFileOpenFileTree() function {{{2
" 
function s:KATFileOpenFileTree(num)
    exec 'python3 ft.openFile(' . a:num . ')'
endfunction



"
" into file (g-f)
"
"
" SECTION: TagList {{{1
"==============================================================================
" KATTagList
"
" Function: s:KATAttachTagList() function {{{2
" This function make the TagList opened if the TagList is closed.
" Then if TagList is closed, it do nothing.
" 
function s:KATAttachTagList()
    python3 tl.attach()
endfunction


" Function: s:KATDetachTagList() function {{{2
" This function make the TagList closed if the TagList is opened.
" Then if TagList is opened, it do nothing.
" 
function s:KATDetachTagList()
    python3 tl.detach()
endfunction

" Function: s:KATToggleTagList() function {{{2
" This function make the TagList closed if the TagList is opened.
" Then if the TagList is opened, oppositely do.
" 
function s:KATToggleTagList()
    python3 tl.toggle()
endfunction

" Function: s:KATGotoTagList() function {{{2
" 
function s:KATGotoTagList(num)
    exec 'python3 tl.goto_tag(' . a:num . ')'
endfunction


" SECTION: Explorer
"==============================================================================
" search (SrcExpr)
" KATExplorer
"
"
" SECTION: Completion
"==============================================================================
" completion
" KATCompletion
"
"
"
" SECTION: Event Procedure {{{1
"==============================================================================
function KATEvent(target)
    if a:target ==? 'AttachFileTree'
        call s:KATAttachFileTree()
    elseif a:target ==? 'DetachFileTree'
        call s:KATDetachFileTree()
    elseif a:target ==? 'ToggleFileTree'
        call s:KATToggleFileTree()
    elseif a:target ==? 'AttachTagList'
        call s:KATAttachTagList()
    elseif a:target ==? 'DetachTagList'
        call s:KATDetachTagList()
    elseif a:target ==? 'ToggleTagList'
        call s:KATToggleTagList()
    elseif a:target ==? 'FileOpenFileTree'
        call s:KATFileOpenFileTree(line("."))
    elseif a:target ==? 'GotoTagList'
        call s:KATGotoTagList(line("."))
    endif
endfunction

"
" SECTION: Default Setup {{{1
"==============================================================================

" SECTION: Mapping and setup menu {{{2
"==============================================================================
function s:CreateMaps(target, description, shortcut)
    let plug = '<Plug>KAT' . a:target

    execute 'nnoremap <silent> ' . plug . ' :call KATEvent("' . a:target . '")<CR>'
    execute 'xnoremap <silent> ' . plug . ' :call KATEvent("' . a:target . '")<CR>'
    if strlen(a:shortcut)
        if g:KATCreateDefaultMappings && !hasmapto(plug, 'n')
            execute 'nmap <leader>]' . a:shortcut . ' ' . plug
        endif
    endif
endfunction

call s:CreateMaps('AttachFileTree',   'AttachFileTree',     '')
call s:CreateMaps('DetachFileTree',   'DetachFileTree',     '')
call s:CreateMaps('ToggleFileTree',   'ToggleFileTree',     'f')
call s:CreateMaps('AttachTagList',   'AttachTagList',     '')
call s:CreateMaps('DetachTagList',   'DetachTagList',     '')
call s:CreateMaps('ToggleTagList',   'ToggleTagList',     't')
call s:CreateMaps('FileOpenFileTree', 'FileOpenFileTree',    '')
call s:CreateMaps('GotoTagList', 'GotoTagList',    '')
