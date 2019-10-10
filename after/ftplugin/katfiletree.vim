if exists("b:current_filetype_plugin")
    finish
endif
let b:current_filetype_plugin = g:KATFiletypeFileTree

setlocal foldmethod=syntax

setlocal foldtext=KATFoldtextFileTree()

function KATFoldtextFileTree()
    let l:line = getline(v:foldstart)
    let l:sub = substitute(line, "▼", "▶", "")
    let l:result = l:sub . repeat(' ', winwidth(0))
    return result
endfunction
