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

if !exists("g:KATMaxTagDepth")
    let g:KATMaxTagDepth = 7
endif

if !exists("g:KATMaxHighlightLineMax")
    syntax sync minlines=100 maxlines=1000
else
    exec 'syntax sync minlines=10 maxlines='.g:KATMaxHighlightLineMax
endif

syntax clear

" syntax match KATTagListSection /=.*=/ contained
" highlight link KATTagListSection PreProc

" syntax region KATTagListHelp start=/^\".*/ end=/^[^\"]\+/me=s-1,re=s-1 fold contains=KATTagListSection
" highlight link KATTagListHelp Constant

" syntax match KATTagListComment /#.*/ contains=KATTagListSection
" highlight link KATTagListComment Comment

highlight Folded ctermbg=NONE ctermfg=10
