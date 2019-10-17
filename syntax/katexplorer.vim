" Vim syntax file
" Language:     kattaglist
" Maintainer:   TOT0Ro  <tot0roprog@gmail.com>
" Last Change:  2019 Oct 8

if exists("b:current_syntax")
    finish
endif

if !exists("g:KATFiletypeExplorer")
    finish
endif

let b:current_syntax = g:KATFiletypeExplorer

syntax clear

syntax match KATExplorerTagname />.*</ contained
highlight link KATExplorerTagname Special

syntax match KATExplorerComment /^=.*=$/ contains=KATExplorerTagname
highlight link KATExplorerComment Underlined

syntax match KATExplorerError /^!!!!!.*!!!!!$/ contains=KATExplorerTagname
highlight link KATExplorerError Error

syntax match KATExplorerTaglist /^[^ \t]\+|[0-9]\+|.*$/
            \ contains=KATExplorerFilename,KATExplorerLineNum |",KATExplorerLine

syntax match KATExplorerFilename /^[A-Za-z0-9_/.-]\+|/me=e-1 contained
            \ nextgroup=KATExplorerLineNum
highlight link KATExplorerFilename Type
syntax match KATExplorerLineNum /[0-9]\+|/me=e-1 contained
highlight link KATExplorerLineNum Statement



highlight Folded ctermbg=NONE ctermfg=10

runtime! syntax/c.vim  |" C style syntax load
