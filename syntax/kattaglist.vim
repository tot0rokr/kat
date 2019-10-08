" Vim syntax file
" Language:     kattaglist
" Maintainer:   TOT0Ro  <tot0roprog@gmail.com>
" Last Change:  2019 Oct 8

if exists("b:current_syntax")
    finish
endif

if !exists("g:KATFiletypeTagList")
    finish
endif

let b:current_syntax = g:KATFiletypeTagList

syntax clear

syntax match KATTagListComment /\".*/
highlight link KATTagListComment Comment

syntax match KATTagListDirectory /[▼▶] [A-Za-z0-9_\.]\+/
highlight link KATTagListDirectory Statement


