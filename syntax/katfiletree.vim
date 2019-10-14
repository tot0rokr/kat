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

if !exists("g:KATMaxFileDepth")
    let g:KATMaxFileDepth = 7
endif

if !exists("g:KATMaxHighlightLineMax")
    syntax sync minlines=100 maxlines=1000
else
    exec 'syntax sync minlines=10 maxlines='.g:KATMaxHighlightLineMax
endif

syntax clear

syntax match KATFileTreeSection /=.*=/ contained
highlight link KATFileTreeSection PreProc

syntax region KATFileTreeHelp start=/^\".*/ end=/^[^\"]\+/me=s-1,re=s-1 fold contains=KATFileTreeSection
highlight link KATFileTreeHelp Constant

syntax match KATFileTreeComment /#.*/ contains=KATFileTreeSection
highlight link KATFileTreeComment Comment


for i in range(0, g:KATMaxFileDepth)
    let s:indentString = repeat('  ', i)
    exec 'syntax region KATFileTreeDirectoryDepth' . i
                \ . ' matchgroup=KATFileTreeDirectoryHighLightStart'
                \ . ' start=/^' . s:indentString . '▼.*/he=e,re=e+1'
                \ . ' skip=/^  ' . s:indentString . '.*/'
                \ . ' matchgroup=KATFileTreeDirectoryHighLightEnd'
                \ . ' end=/^' . s:indentString . '[^ \t]\+/me=s-1,re=s-1'
                \ . ' contains=ALL keepend skipwhite fold'
    " exec 'syntax match KATFileTreeDirectoryDepth' . i
                " \ . ' /^' . s:indentString
                " \ . '▼.*\(\n  ' . s:indentString . '[^ \t]\+\)*/hs=s,he=s'
    " exec 'highlight link KATFileTreeDirectoryDepth' . i . ' Statement'
endfor
exec 'highlight link KATFileTreeDirectoryHighLightStart Statement'


highlight Folded ctermbg=NONE ctermfg=10

