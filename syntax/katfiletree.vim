" Vim syntax file
" Language:     katfiletree
" Maintainer:   TOT0Ro  <tot0roprog@gmail.com>
" Last Change:  2019 Oct 8

if exists("b:current_syntax")
    finish
endif

if !exists("g:KATFiletypeFileTree")
    finish
endif

let b:current_syntax = g:KATFiletypeFileTree

syntax clear

syntax match KATFileTreeComment /\".*/
highlight link KATFileTreeComment Comment

syntax match KATFileTreeDirectory /[▼▶] [A-Za-z0-9_\.]\+/
highlight link KATFileTreeDirectory Statement

