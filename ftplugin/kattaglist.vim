if exists("b:current_filetype_plugin")
    finish
endif
let b:current_filetype_plugin = g:KATFiletypeTagList

setlocal nowrap

setlocal foldmethod=syntax

setlocal foldopen=search,mark

setlocal foldtext=KATFoldtextTagList()


function! KATFoldtextTagList()
    let l:line = getline(v:foldstart)
    let l:sub = substitute(line, "▼", "▶", "")
    let l:result = l:sub . repeat(' ', winwidth(0))
    return result
endfunction

nmap <buffer> ?         gg<Space>|" help
nnoremap <buffer> q     :hide<CR>|" quit
nnoremap <buffer> c     zc|" close
nnoremap <buffer> C     zC|" CLOSE
nnoremap <buffer> o     zo|" open
nnoremap <buffer> O     zO|" OPEN
nnoremap <buffer> p     zr|" reduce (exPand)
nnoremap <buffer> P     zR|" REDUCE (exPand)
nnoremap <buffer> r     zm|" more   (Reduce)
nnoremap <buffer> R     zM|" MORE   (Reduce)
nnoremap <buffer> j     j|" next line
nnoremap <buffer> k     k|" prev line
nnoremap <buffer> J     ]z|" last line of current opened dir
nnoremap <buffer> K     [z|" top line of current opened dir
nnoremap <buffer> L     zj|" next dir
nnoremap <buffer> H     zk|" prev dir
nnoremap <buffer> a     za|" toggle
nnoremap <buffer> A     zA|" toggle
nnoremap <buffer> <Space> za|" toggle
" nmap <buffer> <C-]>     <Plug>KATGotoTagExplorer|" goto tag what is shown by Explorer
" nmap <buffer> g]        <Plug>KATGotoTagExplorer|" goto tag what is shown by Explorer
" nmap <buffer> <leader>g <Plug>KATGotoTagExplorer|" goto tag what is shown by Explorer
nmap <buffer> <Enter>   <Plug>KATGotoTagList|" if tag is matched Explorer
" show matched tag list, then you can choose one by using 'KATSelectTagExplorer' command
